#ifndef ATG_ENGINE_SIM_CAMSHAFT_H
#define ATG_ENGINE_SIM_CAMSHAFT_H

#include "part.h"

#include "function.h"
#include "units.h"

class Crankshaft;
class Camshaft : public Part {
    public:
        struct Parameters {
            // Number of lobes
            int lobes;

            // Camshaft advance in camshaft degrees
            double advance = 0;

            // Corresponding crankshaft
            Crankshaft *crankshaft;

            // Lobe profile
            Function *lobeProfile;

            // Base radius
            double baseRadius = units::distance(600, units::thou);

            // 1 for a four-stroke; 2 makes every lobe act once per crank
            // revolution, for two-stroke valves and piston-controlled ports.
            double lobesPerCycle = 1;
        };

    public:
        Camshaft();
        virtual ~Camshaft();

        void initialize(const Parameters &params);
        virtual void destroy();

        double valveLift(int lobe) const;
        double sampleLobe(double theta) const;

        void setLobeCenterline(int lobe, double crankAngle) { m_lobeAngles[lobe] = crankAngle / 2; }
        double getLobeCenterline(int lobe) const { return m_lobeAngles[lobe]; }

        double getAngle() const;

        Function *getLobeProfile() const { return m_lobeProfile; }
        double getAdvance() const { return m_advance; }
        double getBaseRadius() const { return m_baseRadius; }

    private:
        Crankshaft *m_crankshaft;
        Function *m_lobeProfile;
        double *m_lobeAngles;
        double m_advance;
        double m_baseRadius;
        int m_lobes;
        int m_lobesPerCycle;
};

#endif /* ATG_ENGINE_SIM_CAMSHAFT_H */
