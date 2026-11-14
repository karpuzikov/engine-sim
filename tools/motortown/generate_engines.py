"""Generate one Engine Simulator script per Motor Town engine from motortown_engines.json.

Every value in a generated script is one of three kinds, marked in a comment on its line:
  SOURCED      - found in a cited source (see motortown_engines.json -> sources)
  ESTIMATE     - an unsourced estimate from the data table (not checked against a source)
  PLACEHOLDER  - nothing found; a generic default from PLACEHOLDER_DEFAULTS below

Run:  python tools/motortown/generate_engines.py
Writes assets/engines/motortown/<engine id>.mr and the Motor Town section of README.md (between the motortown markers).
"""
import json
import math
import pathlib
import re

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA_FILE = REPOSITORY_ROOT / "tools" / "motortown" / "motortown_engines.json"
OUTPUT_DIRECTORY = REPOSITORY_ROOT / "assets" / "engines" / "motortown"
README_FILE = REPOSITORY_ROOT / "README.md"
README_START_MARKER = "<!-- motortown:start -->"
README_END_MARKER = "<!-- motortown:end -->"

# Generic defaults used only where no sourced or estimated value exists.
PLACEHOLDER_DEFAULTS = {
    "compression_ratio_petrol": 9.0,
    "compression_ratio_diesel": 17.0,
    "redline_petrol_rpm": 6000,
    "redline_diesel_rpm": 2400,
    "rod_length_to_stroke_ratio": 1.75,
    "rod_length_to_stroke_ratio_flat_engines": 2.0,  # 1.75 makes the flat engines' simulation diverge at start
    "compression_height_to_bore_ratio": 0.40,
    "cam_duration_at_50_thou_deg_petrol": 210,
    "cam_duration_at_50_thou_deg_diesel": 200,
    "cam_lift_thou_petrol": 400,
    "cam_lift_thou_diesel": 350,
    "lobe_separation_deg": 112,
    "exhaust_primary_length_inch": 10.0,
    "idle_air_k_carb_per_litre": 0.7,  # upstream examples leak about 0.5-1 k_carb per litre past the closed throttle
    "idle_air_k_carb_extra": 1.5,  # small engines need relatively more to keep running
    "starter_speed_rpm": 400,
    "simulation_frequency": 20000,
    "diesel_idle_speed_rpm": 650,
    "diesel_injection_timing_deg_btdc": "4 at idle to 12 at the redline",
    "diesel_fuel_conversion_efficiency": 0.40,
    "two_stroke_crankcase_scavenging_pressure_atm": 1.3,
    "two_stroke_blower_pressure_atm": 1.5,
    "two_stroke_exhaust_port_open_deg_before_bdc": 85,
    "two_stroke_transfer_port_open_deg_before_bdc": 60,
    "uniflow_intake_port_open_deg_before_bdc": 48,
    "uniflow_exhaust_valve_center_deg_before_bdc": 15,
    "uniflow_exhaust_duration_at_50_thou_deg": 140,
    "vehicle_mass_kg_petrol": 1500,
    "vehicle_mass_kg_diesel": 12000,
}

# Cylinder numbering per maker: "odd_even" = odd cylinders on the first bank (GM, Chrysler);
# "sequential" = first half of the numbers on the first bank (Ford, Mercedes, Porsche, VW, Lamborghini).
ODD_EVEN_NUMBERED_ENGINES = {"chevy_283", "chevy_350_l48", "chevy_307", "chevy_350_truck", "chevy_305", "chrysler_318_la",
                             "chrysler_360_la", "olds_307", "gm_53_ly5", "chrysler_57_hemi", "buick_lc2"}

# Firing events (crank degrees inside the 720 degree cycle) for engines that are not evenly fired from a plain firing order.
SPECIAL_FIRING_DEGREES = {
    "yamaha_cp4": {1: 0, 3: 270, 2: 450, 4: 540},         # crossplane 270-180-90-180, order 1-3-2-4
    "honda_cb250_k": {1: 0, 2: 180},                       # 180 degree crank: 180/540
    "citroen_602": {1: 0, 2: 360},                         # flat twin, fires every 360
    "subaru_ek23": {1: 0, 2: 360},                         # 360 degree twin
    "detroit_6v92ta": {1: 0, 6: 60, 3: 120, 5: 180, 2: 240, 4: 300},  # two-stroke: 1L-3R-3L-2R-2L-1R with L1-3 = 1-3, R1-3 = 4-6
}

MISSING_FIELD_LABELS = {"bore": "bore", "stroke": "stroke", "cc": "displacement", "cr": "compression ratio", "hp": "power",
                        "hp_rpm": "power rpm", "nm": "torque", "nm_rpm": "torque rpm", "redline": "redline", "fo": "firing order",
                        "bank": "bank angle", "rod": "rod length", "cam_duration": "cam duration", "cam_lift": "cam lift",
                        "valve_in": "intake valve", "valve_ex": "exhaust valve"}


def read_value(engine, field):
    """Return (value, kind) where kind is SOURCED, ESTIMATE or None."""
    source = engine["sources"].get(field)
    if source is not None and source["value"] not in (None, "", "unknown"):
        return source["value"], "SOURCED"
    estimate = engine.get(field)
    if estimate not in (None, "", "unknown"):
        return estimate, "ESTIMATE"
    return None, None


def is_diesel(engine):
    return "diesel" in str(engine.get("fuel", "")).lower()


# Two-stroke engines and how they scavenge: "crankcase" (piston ports, the crankcase pumps the charge)
# or "uniflow" (a blower pushes air through piston ports, exhaust leaves through cam-driven valves).
TWO_STROKE_SCAVENGING = {"detroit_6v92ta": "uniflow", "vespa_px150": "crankcase"}


def is_two_stroke(engine):
    return engine["id"] in TWO_STROKE_SCAVENGING


def fuel_kind(engine):
    return "diesel" if is_diesel(engine) else "petrol"


def value_or_placeholder(engine, field, placeholder_value):
    value, kind = read_value(engine, field)
    if kind is None:
        return placeholder_value, "PLACEHOLDER"
    return value, kind


def numeric(value):
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"-?\d+(\.\d+)?", str(value))
    return float(match.group()) if match else None


def duration_at_50_thou_deg(value):
    """Sources mix advertised and 0.050 in durations; a value in parentheses (e.g. "w/o ramp") is the 0.050 in figure."""
    inside_parentheses = re.search(r"\(([^)]*)\)", str(value))
    if inside_parentheses and numeric(inside_parentheses.group(1)) is not None:
        return numeric(inside_parentheses.group(1))
    return numeric(value)


def lift_in_thou(value):
    """Lift may be given in inches ("0.400 in"), millimetres (e.g. 8.6) or thousandths (e.g. 400)."""
    number = numeric(value)
    if number is None:
        return None
    if re.search(r"\d\s*in\b", str(value)) or number < 1.5:
        return number * 1000
    if number < 30:
        return number / 0.0254
    return number


def bank_layout(engine):
    """Return (bank angles in degrees, cylinder number -> bank index)."""
    layout = engine["layout"].upper()
    cylinder_count = int(engine["cyl"])
    if layout.startswith("I") or cylinder_count == 1:
        return [0.0], {number: 0 for number in range(1, cylinder_count + 1)}
    if layout.startswith("H"):
        included_angle = 180.0
    else:
        bank_value, _ = read_value(engine, "bank")
        included_angle = numeric(bank_value) or 90.0
    angles = [-included_angle / 2.0, included_angle / 2.0]
    if engine["id"] in ODD_EVEN_NUMBERED_ENGINES:
        assignment = {number: (0 if number % 2 == 1 else 1) for number in range(1, cylinder_count + 1)}
    else:
        half = cylinder_count // 2
        assignment = {number: (0 if number <= half else 1) for number in range(1, cylinder_count + 1)}
    return angles, assignment


def firing_degrees(engine):
    """Return (cylinder number -> firing crank angle in degrees, kind of the firing order value)."""
    cylinder_count = int(engine["cyl"])
    if engine["id"] in SPECIAL_FIRING_DEGREES:
        _, kind = read_value(engine, "fo")
        return SPECIAL_FIRING_DEGREES[engine["id"]], kind or "ESTIMATE"
    firing_order_value, kind = read_value(engine, "fo")
    numbers = [int(token) for token in re.findall(r"\d+", str(firing_order_value or ""))]
    if sorted(numbers) != list(range(1, cylinder_count + 1)):
        standard_orders = {1: [1], 2: [1, 2], 3: [1, 3, 2], 4: [1, 3, 4, 2], 5: [1, 2, 4, 5, 3], 6: [1, 5, 3, 6, 2, 4],
                           8: [1, 8, 4, 3, 6, 5, 7, 2] if engine["id"] in ODD_EVEN_NUMBERED_ENGINES else [1, 5, 4, 8, 6, 3, 7, 2]}
        numbers, kind = standard_orders[cylinder_count], "PLACEHOLDER"
    interval = (360.0 if is_two_stroke(engine) else 720.0) / cylinder_count
    return {number: position * interval for position, number in enumerate(numbers)}, kind


def comment(kind, extra=""):
    return f"  // {kind}{(': ' + extra) if extra else ''}"


def build_script(engine):
    engine_id = engine["id"]
    fuel = fuel_kind(engine)
    cylinder_count = int(engine["cyl"])
    bore_mm, bore_kind = read_value(engine, "bore")
    stroke_mm, stroke_kind = read_value(engine, "stroke")
    bore_mm, stroke_mm = numeric(bore_mm), numeric(stroke_mm)
    if bore_mm is None or stroke_mm is None:
        raise ValueError(f"{engine_id}: bore and stroke are required to build a script")
    displacement_per_cylinder_cc = math.pi / 4 * (bore_mm / 10) ** 2 * (stroke_mm / 10)
    displacement_litres = displacement_per_cylinder_cc * cylinder_count / 1000

    compression_ratio, compression_kind = value_or_placeholder(engine, "cr", PLACEHOLDER_DEFAULTS[f"compression_ratio_{fuel}"])
    compression_ratio = numeric(compression_ratio)
    chamber_volume_cc = displacement_per_cylinder_cc / (compression_ratio - 1)
    redline_rpm, redline_kind = value_or_placeholder(engine, "redline", PLACEHOLDER_DEFAULTS[f"redline_{fuel}_rpm"])
    redline_rpm = numeric(redline_rpm)
    rod_ratio = PLACEHOLDER_DEFAULTS["rod_length_to_stroke_ratio_flat_engines" if engine["layout"].upper().startswith("H") else "rod_length_to_stroke_ratio"]
    rod_mm, rod_kind = value_or_placeholder(engine, "rod", round(stroke_mm * rod_ratio, 1))
    rod_mm = numeric(rod_mm)
    compression_height_mm = round(bore_mm * PLACEHOLDER_DEFAULTS["compression_height_to_bore_ratio"], 1)
    deck_height_mm = round(stroke_mm / 2 + rod_mm + compression_height_mm, 1)
    duration_placeholder = PLACEHOLDER_DEFAULTS["uniflow_exhaust_duration_at_50_thou_deg" if is_two_stroke(engine) else f"cam_duration_at_50_thou_deg_{fuel}"]
    cam_duration, cam_duration_kind = value_or_placeholder(engine, "cam_duration", duration_placeholder)
    cam_lift, cam_lift_kind = value_or_placeholder(engine, "cam_lift", PLACEHOLDER_DEFAULTS[f"cam_lift_thou_{fuel}"])
    cam_duration, cam_lift = duration_at_50_thou_deg(cam_duration), lift_in_thou(cam_lift)
    size_scale = displacement_litres / 2.2  # scale relative to upstream's Audi 2.2 i5 example
    bore_scale = bore_mm / 81.0

    angles, bank_of_cylinder = bank_layout(engine)
    firing, firing_kind = firing_degrees(engine)
    first_bank_angle = angles[0]

    lines = []
    add = lines.append
    add('import "engine_sim.mr"')
    add("")
    add("// Generated by tools/motortown/generate_engines.py from tools/motortown/motortown_engines.json. Do not edit by hand.")
    add(f"// {engine['name']}")
    add("// Value kinds: SOURCED (cited source), ESTIMATE (unsourced estimate), PLACEHOLDER (nothing found, generic default).")
    if fuel == "diesel":
        add("// Diesel: fuel injected into the cylinders lights by compression; the pedal meters fuel through the injection pump's governor.")
    if is_two_stroke(engine):
        add(f"// Two-stroke ({TWO_STROKE_SCAVENGING[engine_id]} scavenging): every cylinder fires every revolution.")
    add("")
    add("units units()")
    add("constants constants()")
    add("impulse_response_library ir_lib()")
    add("")
    add(f"private node {engine_id}_wires {{")
    for number in range(1, cylinder_count + 1):
        add(f"    output wire{number}: ignition_wire();")
    add("}")
    add("")
    add("label cycle(2 * 360 * units.deg)")
    add(f"private node {engine_id}_ignition {{")
    add("    input wires;")
    add("    input timing_curve;")
    firings_per_cycle = 2 if is_two_stroke(engine) else 1
    if fuel == "diesel":
        idle_speed_rpm, idle_kind = value_or_placeholder(engine, "idle", PLACEHOLDER_DEFAULTS["diesel_idle_speed_rpm"])
        governed_rpm, governed_kind = read_value(engine, "hp_rpm")
        governed_rpm = numeric(governed_rpm) or redline_rpm
        power_hp, power_kind = read_value(engine, "hp")
        injections_per_second = cylinder_count * governed_rpm / 60 / (1 if is_two_stroke(engine) else 2)
        fuel_per_injection_mg = (numeric(power_hp) * 745.7 / (PLACEHOLDER_DEFAULTS["diesel_fuel_conversion_efficiency"] * 42.8e6)
                                 / injections_per_second * 1e6)
        add("    alias output __out:")
        add("        diesel_injection_pump(")
        add("            timing_curve: timing_curve,")
        add(f"            max_fuel_per_injection: {fuel_per_injection_mg:.1f} * units.g / 1000,  // derived: rated power ({power_kind}) at 40% efficiency (PLACEHOLDER)")
        add(f"            idle_speed: {numeric(idle_speed_rpm):.0f} * units.rpm,{comment(idle_kind)}")
        add(f"            governed_speed: {governed_rpm:.0f} * units.rpm,  // rated speed ({governed_kind or 'PLACEHOLDER'})")
        add(f"            firings_per_cycle: {firings_per_cycle}")
        add("        )")
    else:
        add(f"    input rev_limit: {redline_rpm:.0f} * units.rpm;")
        add("    alias output __out:")
        add(f"        ignition_module(timing_curve: timing_curve, rev_limit: rev_limit, firings_per_cycle: {firings_per_cycle})")
    ordered = sorted(firing.items(), key=lambda item: item[1])
    for index, (number, degrees) in enumerate(ordered):
        terminator = ";" if index == len(ordered) - 1 else ""
        add(f"            .connect_wire(wires.wire{number}, ({degrees:.1f} / 720.0) * cycle){terminator}")
    add(f"}}  // firing order {firing_kind}")
    add("")
    add(f"public node {engine_id} {{")
    add("    alias output __out: engine;")
    add(f"    {engine_id}_wires wires()")
    add("")
    add("    engine engine(")
    add(f"        name: \"{engine['name']}\",")
    add(f"        starter_torque: {200 * max(size_scale, 0.3):.0f} * units.lb_ft,  // PLACEHOLDER")
    add(f"        starter_speed: {PLACEHOLDER_DEFAULTS['starter_speed_rpm']} * units.rpm,  // PLACEHOLDER")
    add(f"        redline: {redline_rpm:.0f} * units.rpm,{comment(redline_kind)}")
    add(f"        simulation_frequency: {PLACEHOLDER_DEFAULTS['simulation_frequency']},  // PLACEHOLDER")
    if fuel == "diesel":
        add("        fuel: diesel_fuel()")
    else:
        add("        fuel: fuel(max_turbulence_effect: 4.0, burning_efficiency_randomness: 0.2, max_burning_efficiency: 0.85)  // PLACEHOLDER")
    add("    )")
    add("")
    add("    crankshaft c0(")
    add(f"        throw: {stroke_mm / 2:.2f} * units.mm,{comment(stroke_kind, 'half the stroke')}")
    add(f"        flywheel_mass: {20 * max(size_scale, 0.25):.1f} * units.lb,  // PLACEHOLDER")
    add(f"        mass: {40 * max(size_scale, 0.2):.1f} * units.lb,  // PLACEHOLDER")
    add(f"        friction_torque: {max(0.5, 10 * size_scale):.1f} * units.lb_ft,  // PLACEHOLDER")
    add(f"        moment_of_inertia: {0.207 * max(size_scale, 0.15):.4f},  // PLACEHOLDER")
    add("        position_x: 0.0,")
    add("        position_y: 0.0,")
    add(f"        tdc: {90 + first_bank_angle:.1f} * units.deg")
    add("    )")
    add("")
    for number in range(1, cylinder_count + 1):
        journal_angle = (firing[number] + (angles[bank_of_cylinder[number]] - first_bank_angle)) % 360.0
        add(f"    rod_journal rj{number}(angle: {journal_angle:.1f} * units.deg)")
    add("    c0")
    for number in range(1, cylinder_count + 1):
        add(f"        .add_rod_journal(rj{number})")
    add("")
    add("    piston_parameters piston_params(")
    add(f"        mass: {400 * bore_scale ** 3:.0f} * units.g,  // PLACEHOLDER")
    add("        blowby: 0,")
    add(f"        compression_height: {compression_height_mm} * units.mm,  // PLACEHOLDER")
    add("        wrist_pin_position: 0 * units.mm,")
    add("        displacement: 0.0")
    add("    )")
    add("")
    add("    connecting_rod_parameters cr_params(")
    add(f"        mass: {300 * bore_scale ** 3:.0f} * units.g,  // PLACEHOLDER")
    add(f"        moment_of_inertia: {0.0015884918 * bore_scale ** 5:.6f},  // PLACEHOLDER")
    add("        center_of_mass: 0.0,")
    add(f"        length: {rod_mm} * units.mm{comment(rod_kind)}")
    add("    )")
    add("")
    add("    cylinder_bank_parameters bank_params(")
    add(f"        bore: {bore_mm} * units.mm,{comment(bore_kind)}")
    add(f"        deck_height: {deck_height_mm} * units.mm  // derived: half stroke + rod + compression height")
    add("    )")
    add("")
    add("    intake intake(")
    add(f"        plenum_volume: {max(1.0, 2.3 * size_scale):.1f} * units.L,  // PLACEHOLDER")
    add(f"        plenum_cross_section_area: {max(5.0, 10.0 * size_scale):.1f} * units.cm2,  // PLACEHOLDER")
    add(f"        intake_flow_rate: k_carb({500 * size_scale:.0f}),  // PLACEHOLDER")
    add("        idle_flow_rate: k_carb(0.0),")
    intake_flow_k_carb = 500 * size_scale
    idle_air_k_carb = PLACEHOLDER_DEFAULTS["idle_air_k_carb_per_litre"] * displacement_litres + PLACEHOLDER_DEFAULTS["idle_air_k_carb_extra"]
    supply_line = ""
    if is_two_stroke(engine):
        scavenging = TWO_STROKE_SCAVENGING[engine_id]
        pressure = PLACEHOLDER_DEFAULTS["two_stroke_blower_pressure_atm" if scavenging == "uniflow" else "two_stroke_crankcase_scavenging_pressure_atm"]
        supply_line = f"        supply_pressure: {pressure} * units.atm  // PLACEHOLDER: {'blower' if scavenging == 'uniflow' else 'crankcase pumping'}"
    add(f"        idle_throttle_plate_position: {1 - idle_air_k_carb / intake_flow_k_carb:.4f}{',' if supply_line else ''}  // PLACEHOLDER: idle air {idle_air_k_carb:.1f} k_carb")
    if supply_line:
        add(supply_line)
    add("    )")
    add("")
    add("    exhaust_system_parameters es_params(")
    add(f"        outlet_flow_rate: k_carb({300 * size_scale:.0f}),  // PLACEHOLDER")
    add(f"        primary_tube_length: {PLACEHOLDER_DEFAULTS['exhaust_primary_length_inch']} * units.inch,  // PLACEHOLDER")
    add(f"        primary_flow_rate: k_carb({100 * size_scale:.0f}),  // PLACEHOLDER")
    add("        velocity_decay: 0.5,  // PLACEHOLDER")
    add(f"        volume: {max(10.0, 50.0 * size_scale):.0f} * units.L  // PLACEHOLDER")
    add("    )")
    for bank_index in range(len(angles)):
        add(f"    exhaust_system exhaust{bank_index}(es_params, audio_volume: 1.0, impulse_response: ir_lib.default_0)  // PLACEHOLDER")
    add("")
    for bank_index, angle in enumerate(angles):
        add(f"    cylinder_bank b{bank_index}(bank_params, angle: {angle:.1f} * units.deg)")
        add(f"    b{bank_index}")
        for number in range(1, cylinder_count + 1):
            if bank_of_cylinder[number] != bank_index:
                continue
            add("        .add_cylinder(")
            add("            piston: piston(piston_params, blowby: k_28inH2O(0.3)),")
            add("            connecting_rod: connecting_rod(cr_params),")
            add(f"            rod_journal: rj{number},")
            add("            intake: intake,")
            add(f"            exhaust_system: exhaust{bank_index},")
            add(f"            ignition_wire: wires.wire{number}")
            add("        )")
        add(f"    engine.add_cylinder_bank(b{bank_index})")
        add("")
    add("    engine.add_crankshaft(c0)")
    add("")
    add(f"    harmonic_cam_lobe lobe(duration_at_50_thou: {cam_duration:.0f} * units.deg, gamma: 1.0, lift: {cam_lift:.0f} * units.thou, steps: 100)"
        f"  // duration {cam_duration_kind}, lift {cam_lift_kind}")
    add(f"    label lobe_separation({PLACEHOLDER_DEFAULTS['lobe_separation_deg']} * units.deg)  // PLACEHOLDER")
    add("    label rot360(360 * units.deg)")
    add(f"    camshaft_parameters cam_params(advance: 0 * units.deg, base_radius: 0.75 * units.inch, lobes_per_cycle: {2 if is_two_stroke(engine) else 1})  // PLACEHOLDER base radius")
    for bank_index in range(len(angles)):
        numbers = [number for number in range(1, cylinder_count + 1) if bank_of_cylinder[number] == bank_index]
        if is_two_stroke(engine):
            port_profile = "piston_port_lobe(stroke: {stroke} * units.mm, rod_length: {rod} * units.mm, open_before_bdc: {open} * units.deg)"
            if TWO_STROKE_SCAVENGING[engine_id] == "crankcase":
                intake_profile = port_profile.format(stroke=stroke_mm, rod=rod_mm, open=PLACEHOLDER_DEFAULTS["two_stroke_transfer_port_open_deg_before_bdc"])
                exhaust_profile = port_profile.format(stroke=stroke_mm, rod=rod_mm, open=PLACEHOLDER_DEFAULTS["two_stroke_exhaust_port_open_deg_before_bdc"])
                exhaust_center = 180
                add("    // PLACEHOLDER port timings: transfer and exhaust ports opened by the piston")
            else:
                intake_profile = port_profile.format(stroke=stroke_mm, rod=rod_mm, open=PLACEHOLDER_DEFAULTS["uniflow_intake_port_open_deg_before_bdc"])
                exhaust_profile = "lobe"
                exhaust_center = 180 - PLACEHOLDER_DEFAULTS["uniflow_exhaust_valve_center_deg_before_bdc"]
                add("    // PLACEHOLDER timings: intake ports opened by the piston, exhaust valves driven by the camshaft")
            add(f"    camshaft intake_cam_{bank_index}(cam_params, lobe_profile: {intake_profile})")
            add(f"    camshaft exhaust_cam_{bank_index}(cam_params, lobe_profile: {exhaust_profile})")
            add(f"    intake_cam_{bank_index}")
            for number in numbers:
                add(f"        .add_lobe({firing[number] + 180:.1f} * units.deg)")
            add(f"    exhaust_cam_{bank_index}")
            for number in numbers:
                add(f"        .add_lobe({firing[number] + exhaust_center:.1f} * units.deg)")
        else:
            add(f"    camshaft intake_cam_{bank_index}(cam_params, lobe_profile: lobe)")
            add(f"    camshaft exhaust_cam_{bank_index}(cam_params, lobe_profile: lobe)")
            add(f"    intake_cam_{bank_index}")
            for number in numbers:
                add(f"        .add_lobe(rot360 + lobe_separation + {firing[number]:.1f} * units.deg)")
            add(f"    exhaust_cam_{bank_index}")
            for number in numbers:
                add(f"        .add_lobe(rot360 - lobe_separation + {firing[number]:.1f} * units.deg)")
        add(f"    b{bank_index}.set_cylinder_head(")
        add("        generic_small_engine_head(")
        add(f"            chamber_volume: {chamber_volume_cc:.1f} * units.cc,  // from compression ratio {compression_ratio} ({compression_kind})")
        add(f"            flow_attenuation: {bore_scale ** 2:.2f},  // PLACEHOLDER: scaled with bore area")
        add(f"            intake_camshaft: intake_cam_{bank_index},")
        add(f"            exhaust_camshaft: exhaust_cam_{bank_index}{', flip_display: true' if bank_index == 1 else ''}")
        add("        )")
        add("    )")
    add("")
    add(f"    function timing_curve({redline_rpm / 6:.0f} * units.rpm)  // PLACEHOLDER curve" + (" (start of injection)" if fuel == "diesel" else ""))
    add("    timing_curve")
    for step, degrees in enumerate([4, 4, 6, 8, 10, 12, 12] if fuel == "diesel" else [12, 12, 20, 26, 30, 34, 38]):
        add(f"        .add_sample({redline_rpm * step / 6:.0f} * units.rpm, {degrees} * units.deg)")
    add("")
    add(f"    engine.add_ignition_module({engine_id}_ignition(wires: wires, timing_curve: timing_curve))")
    add("}")
    add("")
    vehicle_mass_kg = PLACEHOLDER_DEFAULTS[f"vehicle_mass_kg_{fuel}"]
    add(f"private node {engine_id}_vehicle {{  // PLACEHOLDER vehicle")
    add("    alias output __out:")
    add(f"        vehicle(mass: {vehicle_mass_kg} * units.kg, drag_coefficient: 0.5, cross_sectional_area: (80 * units.inch) * (70 * units.inch),")
    add(f"                diff_ratio: {5.0 if fuel == 'diesel' else 3.9}, tire_radius: {18 if fuel == 'diesel' else 12} * units.inch,")
    add(f"                rolling_resistance: 0.015 * {vehicle_mass_kg} * units.kg * 9.81);")
    add("}")
    add("")
    add(f"private node {engine_id}_transmission {{  // PLACEHOLDER transmission")
    add("    alias output __out:")
    add(f"        transmission(max_clutch_torque: {max(300, 300 * size_scale):.0f} * units.lb_ft)")
    add("        .add_gear(3.5).add_gear(2.1).add_gear(1.4).add_gear(1.0).add_gear(0.8);")
    add("}")
    add("")
    add("public node main {")
    add(f"    set_engine({engine_id}())")
    add(f"    set_vehicle({engine_id}_vehicle())")
    add(f"    set_transmission({engine_id}_transmission())")
    add("}")
    return "\n".join(lines) + "\n"


def missing_fields(engine):
    fields = ["bore", "stroke", "cc", "cr", "hp", "hp_rpm", "nm", "nm_rpm", "redline", "fo", "rod", "cam_duration", "cam_lift", "valve_in", "valve_ex"]
    if engine["layout"].upper().startswith("V"):  # flat engines are 180 degrees by definition
        fields.insert(0, "bank")
    unsourced = [MISSING_FIELD_LABELS[field] for field in fields if field not in engine["sources"]]
    return unsourced


GAME_LAYOUT_PATTERN = re.compile(r"\b(V8|V12|I4|i4|H2)\b")


def game_horsepower(game_engine_name):
    match = re.search(r"(\d+)\s*HP", game_engine_name)
    return int(match.group(1)) if match else None


def build_placeholder_table():
    lines = ["| Placeholder | Value |", "|---|---|"]
    for name, value in PLACEHOLDER_DEFAULTS.items():
        lines.append(f"| {name} | {value} |")
    return lines


def build_report(data):
    engines = {engine["id"]: engine for engine in data["engines"]}
    lines = ["## Motor Town engines", "",
             "Engine scripts for every engine of the game [Motor Town](https://store.steampowered.com/app/1369670/Motor_Town_Behind_The_Wheel/), "
             "built from the real engine of each vehicle the game's vehicles are based on.", "",
             "- Scripts: `assets/engines/motortown/<engine id>.mr`. To run one, change the third line of `assets/main.mr` to "
             "`import \"engines/motortown/<engine id>.mr\"`.",
             "- Data with a source link per value: `tools/motortown/motortown_engines.json`.",
             "- Scripts and this section are generated: `python tools/motortown/generate_engines.py`.", "",
             "Every value in a script carries a comment: **SOURCED** (cited source), **ESTIMATE** (unsourced estimate) or "
             "**PLACEHOLDER** (nothing found, generic default below). Placeholders exist so every engine runs; replace them as data is found.", "",
             "Diesels use this fork's compression ignition (`diesel_injection_pump`, `diesel_fuel`); the Detroit 6V92TA and the Vespa use its "
             "two-stroke support (`firings_per_cycle`, `lobes_per_cycle`, `piston_port_lobe`, intake `supply_pressure`).", "",
             "Status (headless test, 2026-11-13): 67 of 68 scripts start, idle and rev. The Honda CB250 twin does not start yet. "
             "Idle speeds: diesels 680-770 rpm (governor), petrol engines 900-1400 rpm and small engines up to 2000 rpm (placeholder idle air); "
             "the Vespa idles near 3700 rpm (placeholder crankcase pressure).", "",
             "### Placeholders", "",
             "Crank, piston and rod masses, inertia, intake and exhaust flow rates and volumes have no sources for any engine: they are "
             "scaled from upstream's Audi 2.2 i5 example by displacement (or bore for pistons and rods). Vehicle and gearbox are generic. "
             "Timing curve is upstream's i5 curve stretched to the redline. Fixed placeholders:", ""] + build_placeholder_table() + ["",
             "### Missing information", "",
             "Every engine-sim value without a source. The generated scripts use an unsourced estimate or a generic placeholder for these.",
             "Exhaust (header and pipe lengths, muffler volumes) is missing for every engine and is not listed per row.", "",
             "| Engine | Used by | Missing (no source) |", "|---|---|---|"]
    users = {}
    for row in data["vehicle_engine"]:
        for engine_id in row["engine_ids"]:
            users.setdefault(engine_id, []).append(row["real_vehicle"])
    for engine_id, engine in engines.items():
        lines.append(f"| {engine['name']} | {', '.join(users.get(engine_id, []))} | {', '.join(missing_fields(engine)) or '—'} |")
    lines += ["", "### Game vs reality", "",
              "Where the game's engine (name, power, fuel) does not match the real vehicle's engine used here.", "",
              "| Game vehicle | Real vehicle | Game engine | Real engine | Mismatch |", "|---|---|---|---|---|"]
    seen = set()
    for vehicle in data["game_vehicles"]:
        key = (vehicle["inspiration"], vehicle["game_engine"])
        if key in seen:
            continue
        seen.add(key)
        mapping = next((row for row in data["vehicle_engine"] if row["real_vehicle"] == vehicle["inspiration"]), None)
        if mapping is None:
            continue
        game_power = game_horsepower(vehicle["game_engine"])
        candidates = [engines[engine_id] for engine_id in mapping["engine_ids"]]
        real = min(candidates, key=lambda candidate: abs((numeric(read_value(candidate, "hp")[0]) or 0) - (game_power or 0)))
        notes = []
        real_power, _ = read_value(real, "hp")
        real_power = numeric(real_power)
        if game_power and real_power and abs(game_power - real_power) / real_power > 0.15:
            notes.append(f"power {game_power} hp in game vs {real_power:.0f} hp real")
        game_fuel = vehicle["fuel"].lower()
        if game_fuel in ("diesel", "gasoline", "petrol") and (game_fuel == "diesel") != is_diesel(real):
            notes.append(f"fuel {vehicle['fuel']} in game vs {real['fuel']} real")
        layout_match = GAME_LAYOUT_PATTERN.search(vehicle["game_engine"])
        if layout_match and layout_match.group(1).upper().replace("H2", "H2") != real["layout"].upper():
            notes.append(f"layout {layout_match.group(1).upper()} in game vs {real['layout']} real")
        if "UNRESOLVED" in mapping["engine"] or "stand-in" in mapping["engine"] or "tuned to game" in mapping["engine"]:
            notes.append(mapping["engine"])
        if notes:
            lines.append(f"| {vehicle['name']} | {vehicle['inspiration']} | {vehicle['game_engine']} ({vehicle['fuel']}) | {real['name']} | {'; '.join(notes)} |")
    return "\n".join(lines) + "\n"


def main():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for engine in data["engines"]:
        (OUTPUT_DIRECTORY / f"{engine['id']}.mr").write_text(build_script(engine), encoding="utf-8")
    readme = README_FILE.read_text(encoding="utf-8")
    start, end = readme.index(README_START_MARKER), readme.index(README_END_MARKER)
    readme = readme[:start + len(README_START_MARKER)] + "\n" + build_report(data) + readme[end:]
    README_FILE.write_text(readme, encoding="utf-8")
    print(f"wrote {len(data['engines'])} engine scripts and the README section")


if __name__ == "__main__":
    main()
