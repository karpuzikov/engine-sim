#include <gtest/gtest.h>

#include "../include/ignition_module.h"
#include "../include/crankshaft.h"
#include "../include/function.h"
#include "../include/units.h"

namespace {

double fuelAtSpeed(double rpm, double pedal) {
    Crankshaft crankshaft;
    crankshaft.m_body.v_theta = -units::rpm(rpm);

    Function timingCurve;
    timingCurve.initialize(1, units::rpm(1000));
    timingCurve.addSample(0.0, 0.0);

    IgnitionModule::Parameters params;
    params.cylinderCount = 1;
    params.crankshaft = &crankshaft;
    params.timingCurve = &timingCurve;
    params.compressionIgnition = true;
    params.maxFuelPerInjection = units::mass(100, units::g) / 1000;
    params.idleSpeed = units::rpm(600);
    params.governedSpeed = units::rpm(2000);

    IgnitionModule pump;
    pump.initialize(params);
    const double fuel = pump.calculateFuelPerInjection(pedal);
    pump.destroy();
    timingCurve.destroy();
    return fuel / (units::mass(1, units::g) / 1000);  // mg
}

}  // namespace

TEST(DieselGovernorTests, CrankingGetsFullFuel) {
    EXPECT_NEAR(fuelAtSpeed(150, 0.0), 100.0, 1E-6);
}

TEST(DieselGovernorTests, NoIdleFuelAboveTenPercentOverIdle) {
    EXPECT_NEAR(fuelAtSpeed(700, 0.0), 0.0, 1E-6);
}

TEST(DieselGovernorTests, PedalMetersFuelBelowGovernedSpeed) {
    EXPECT_NEAR(fuelAtSpeed(1500, 0.5), 50.0, 1E-6);
}

TEST(DieselGovernorTests, MaximumSpeedGovernorCutsFuel) {
    EXPECT_NEAR(fuelAtSpeed(2100, 1.0), 50.0, 1E-6);
    EXPECT_NEAR(fuelAtSpeed(2200, 1.0), 0.0, 1E-6);
}
