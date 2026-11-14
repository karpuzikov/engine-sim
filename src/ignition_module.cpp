#include "../include/ignition_module.h"

#include "../include/utilities.h"
#include "../include/constants.h"
#include "../include/units.h"

#include <cmath>

IgnitionModule::IgnitionModule() {
    m_plugs = nullptr;
    m_crankshaft = nullptr;
    m_timingCurve = nullptr;
    m_cylinderCount = 0;
    m_lastCrankshaftAngle = 0.0;
    m_enabled = false;
    m_revLimitTimer = 0.0;
    m_revLimit = 0;
    m_limiterDuration = 0;
    m_sparksPerCycle = 1;
    m_compressionIgnition = false;
    m_maxFuelPerInjection = 0;
    m_idleSpeed = 0;
    m_governedSpeed = 0;
    m_autoignitionTemperature = 0;
}

IgnitionModule::~IgnitionModule() {
    assert(m_plugs == nullptr);
}

void IgnitionModule::destroy() {
    delete[] m_plugs;

    m_plugs = nullptr;
    m_cylinderCount = 0;
}

void IgnitionModule::initialize(const Parameters &params) {
    m_cylinderCount = params.cylinderCount;
    m_plugs = new SparkPlug[m_cylinderCount];
    m_crankshaft = params.crankshaft;
    m_timingCurve = params.timingCurve;
    m_revLimit = params.revLimit;
    m_limiterDuration = params.limiterDuration;
    m_sparksPerCycle = static_cast<int>(params.sparksPerCycle);
    m_compressionIgnition = params.compressionIgnition;
    m_maxFuelPerInjection = params.maxFuelPerInjection;
    m_idleSpeed = params.idleSpeed;
    m_governedSpeed = params.governedSpeed;
    m_autoignitionTemperature = params.autoignitionTemperature;
}

void IgnitionModule::setFiringOrder(int cylinderIndex, double angle) {
    assert(cylinderIndex < m_cylinderCount);

    m_plugs[cylinderIndex].angle = angle;
    m_plugs[cylinderIndex].enabled = true;
}

void IgnitionModule::reset() {
    m_lastCrankshaftAngle = m_crankshaft->getCycleAngle();
    resetIgnitionEvents();
}

void IgnitionModule::update(double dt) {
    const double cycleAngle = m_crankshaft->getCycleAngle();

    if (m_enabled && m_revLimitTimer == 0) {
        const double fourPi = 4 * constants::pi;
        const double advance = getTimingAdvance();

        for (int spark = 0; spark < m_sparksPerCycle * m_cylinderCount; ++spark) {
            const int i = spark % m_cylinderCount;
            const double repeat = (spark / m_cylinderCount) * fourPi / m_sparksPerCycle;
            double adjustedAngle = positiveMod(m_plugs[i].angle + repeat - advance, fourPi);
            const double r0 = m_lastCrankshaftAngle;
            double r1 = cycleAngle;

            if (m_crankshaft->m_body.v_theta < 0) {
                if (r1 < r0) {
                    r1 += fourPi;
                    adjustedAngle += fourPi;
                }

                if (adjustedAngle >= r0 && adjustedAngle < r1) {
                    m_plugs[i].ignitionEvent = m_plugs[i].enabled;
                }
            }
            else {
                if (r1 > r0) {
                    r1 -= fourPi;
                    adjustedAngle -= fourPi;
                }

                if (adjustedAngle >= r1 && adjustedAngle < r0) {
                    m_plugs[i].ignitionEvent = m_plugs[i].enabled;
                }
            }
        }
    }

    m_revLimitTimer -= dt;
    if (std::fabs(m_crankshaft->m_body.v_theta) > m_revLimit) {
        m_revLimitTimer = m_limiterDuration;
    }

    if (m_revLimitTimer < 0) {
        m_revLimitTimer = 0;
    }

    m_lastCrankshaftAngle = cycleAngle;
}

bool IgnitionModule::getIgnitionEvent(int index) const {
    return m_plugs[index].ignitionEvent;
}

void IgnitionModule::resetIgnitionEvents() {
    for (int i = 0; i < m_cylinderCount; ++i) {
        m_plugs[i].ignitionEvent = false;
    }
}

double IgnitionModule::calculateFuelPerInjection(double pedal) const {
    const double speed = std::abs(m_crankshaft->m_body.v_theta);

    // Idle governor: full fuel while cranking, none above 110% of idle speed.
    const double idleFuel = clamp((1.1 * m_idleSpeed - speed) / (0.3 * m_idleSpeed));

    // Maximum-speed governor: full fuel up to the governed speed, none above 110% of it.
    const double governorCut = clamp((1.1 * m_governedSpeed - speed) / (0.1 * m_governedSpeed));

    return std::fmax(clamp(pedal), idleFuel) * governorCut * m_maxFuelPerInjection;
}

double IgnitionModule::getTimingAdvance() {
    return m_timingCurve->sampleTriangle(-m_crankshaft->m_body.v_theta);
}

IgnitionModule::SparkPlug *IgnitionModule::getPlug(int i) {
    return &m_plugs[((i % m_cylinderCount) + m_cylinderCount) % m_cylinderCount];
}
