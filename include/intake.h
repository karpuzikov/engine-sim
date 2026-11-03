#ifndef ATG_ENGINE_SIM_INTAKE_H
#define ATG_ENGINE_SIM_INTAKE_H

#include "part.h"

#include "gas_system.h"
#include "units.h"

class Intake : public Part {
    public:
        struct Parameters {
            // Plenum volume
            double volume;

            // Plenum dimensions
            double CrossSectionArea;

            // Input flow constant
            double InputFlowK;

            // Idle-circuit flow constant
            double IdleFlowK;

            // Flow rate from plenum to runner
            double RunnerFlowRate;

            // Molecular air fuel ratio (defaults to ideal for octane)
            double MolecularAfr = (25.0 / 2.0);

            // Throttle plate position at idle
            double IdleThrottlePlatePosition = 0.975;

            // Runner volume
            double RunnerLength = units::distance(4.0, units::inch);

            // Velocity decay factor
            double VelocityDecay = 0.5;

            // Air source upstream of the throttle: the atmosphere, or a
            // blower, supercharger, turbocharger or two-stroke crankcase.
            double SupplyPressure = units::pressure(1.0, units::atm);
            double SupplyTemperature = units::celcius(25.0);
        };

    public:
        Intake();
        virtual ~Intake();

        void initialize(Parameters &params);
        virtual void destroy();

        void process(double dt);

        inline double getRunnerFlowRate() const { return m_runnerFlowRate; }
        inline double getThrottlePlatePosition() const { return m_idleThrottlePlatePosition * m_throttle; }
        inline double getRunnerLength() const { return m_runnerLength; }
        inline double getPlenumCrossSectionArea() const { return m_crossSectionArea; }
        inline double getVelocityDecay() const { return m_velocityDecay; }
        inline double getSupplyPressure() const { return m_supplyPressure; }
        inline void setSupplyPressure(double pressure) { m_supplyPressure = pressure; }
        inline double getSupplyTemperature() const { return m_supplyTemperature; }
        inline void setSupplyTemperature(double temperature) { m_supplyTemperature = temperature; }
        // Oxygen molecules per fuel molecule (before the fixed 0.8 enrichment).
        // A diesel host leans this out at part load: diesels meter fuel, not air.
        inline double getMolecularAfr() const { return m_molecularAfr; }
        inline void setMolecularAfr(double afr) { m_molecularAfr = afr; }

        GasSystem m_system;
        double m_throttle;

        double m_flow;
        double m_flowRate;
        double m_totalFuelInjected;

    protected:
        double m_crossSectionArea;
        double m_inputFlowK;
        double m_idleFlowK;
        double m_runnerFlowRate;
        double m_molecularAfr;
        double m_idleThrottlePlatePosition;
        double m_runnerLength;
        double m_velocityDecay;
        double m_supplyPressure;
        double m_supplyTemperature;

        GasSystem m_atmosphere;
};

#endif /* ATG_ENGINE_SIM_INTAKE_H */
