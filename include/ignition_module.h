#ifndef ATG_ENGINE_SIM_IGNITION_MODULE_H
#define ATG_ENGINE_SIM_IGNITION_MODULE_H

#include "part.h"

#include "crankshaft.h"
#include "function.h"
#include "units.h"

class IgnitionModule : public Part {
    public:
        struct Parameters {
            int cylinderCount;
            Crankshaft *crankshaft;
            Function *timingCurve;
            double revLimit = units::rpm(6000.0);
            double limiterDuration = 0.5 * units::sec;
            // 1 for a four-stroke, 2 for a two-stroke (fires every revolution).
            double firingsPerCycle = 1;

            // Compression ignition (diesel): the timing curve times fuel
            // injection instead of a spark. The injected charge lights only if
            // the compressed air is at least autoignitionTemperature. The fuel
            // per injection is metered by a governor: the pedal sets it up to
            // maxFuelPerInjection, the idle governor adds fuel below idleSpeed
            // and the maximum-speed governor cuts it above governedSpeed.
            bool compressionIgnition = false;
            double maxFuelPerInjection = 0;
            double idleSpeed = 0;
            double governedSpeed = 0;
            double autoignitionTemperature = units::celcius(210.0);
        };

        struct SparkPlug {
            double angle = 0;
            bool ignitionEvent = false;
            bool enabled = false;
        };

    public:
        IgnitionModule();
        virtual ~IgnitionModule();

        virtual void destroy();

        void initialize(const Parameters &params);
        void setFiringOrder(int cylinderIndex, double angle);
        void reset();
        void update(double dt);

        bool getIgnitionEvent(int index) const;
        void resetIgnitionEvents();

        double getTimingAdvance();

        bool isCompressionIgnition() const { return m_compressionIgnition; }
        double getAutoignitionTemperature() const { return m_autoignitionTemperature; }
        double calculateFuelPerInjection(double pedal) const;

        bool m_enabled;

    protected:
        SparkPlug *getPlug(int i);

        Function *m_timingCurve;
        SparkPlug *m_plugs;
        Crankshaft *m_crankshaft;
        int m_cylinderCount;

        double m_lastCrankshaftAngle;
        double m_revLimit;
        double m_revLimitTimer;
        double m_limiterDuration;
        int m_firingsPerCycle;

        bool m_compressionIgnition;
        double m_maxFuelPerInjection;
        double m_idleSpeed;
        double m_governedSpeed;
        double m_autoignitionTemperature;
};

#endif /* ATG_ENGINE_SIM_IGNITION_MODULE_H */
