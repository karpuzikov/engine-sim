#ifndef ATG_ENGINE_SIM_IGNITION_MODULE_NODE_H
#define ATG_ENGINE_SIM_IGNITION_MODULE_NODE_H

#include "object_reference_node.h"

#include "engine_context.h"
#include "function_node.h"

#include "engine_sim.h"

#include <map>

namespace es_script {

    class IgnitionModuleNode : public ObjectReferenceNode<IgnitionModuleNode> {
    public:
        struct Post {
            IgnitionWireNode *wire;
            double angle;
        };

    public:
        IgnitionModuleNode() { /* void */ }
        virtual ~IgnitionModuleNode() { /* void */ }

        void generate(Engine *engine, EngineContext *context) const {
            IgnitionModule::Parameters params;
            params.crankshaft = engine->getCrankshaft(0);
            params.cylinderCount = engine->getCylinderCount();
            params.revLimit = m_revLimit;
            params.timingCurve = m_timingCurve->generate(context);
            params.cylinderCount = engine->getCylinderCount();
            params.limiterDuration = m_limiterDuration;
            params.firingsPerCycle = m_firingsPerCycle;
            params.compressionIgnition = m_compressionIgnition;
            params.maxFuelPerInjection = m_maxFuelPerInjection;
            params.idleSpeed = m_idleSpeed;
            params.governedSpeed = m_governedSpeed;
            params.autoignitionTemperature = m_autoignitionTemperature;
            engine->getIgnitionModule()->initialize(params);

            for (const Post &post : m_posts) {
                std::set<IgnitionWireNode::Connection> connections =
                    post.wire->getConnections();
                for (const IgnitionWireNode::Connection &connection : connections) {
                    const int index = context->getCylinderIndex(
                        connection.first,
                        connection.second
                    );

                    engine->getIgnitionModule()->setFiringOrder(index, post.angle);
                }
            }
        }

        void connect(IgnitionWireNode *wire, double angle) {
            m_posts.push_back({ wire, angle });
        }

    protected:
        virtual void registerInputs() {
            addInput("timing_curve", &m_timingCurve);
            addInput("rev_limit", &m_revLimit);
            addInput("limiter_duration", &m_limiterDuration);
            addInput("firings_per_cycle", &m_firingsPerCycle);
            addInput("compression_ignition", &m_compressionIgnition);
            addInput("max_fuel_per_injection", &m_maxFuelPerInjection);
            addInput("idle_speed", &m_idleSpeed);
            addInput("governed_speed", &m_governedSpeed);
            addInput("autoignition_temperature", &m_autoignitionTemperature);

            ObjectReferenceNode<IgnitionModuleNode>::registerInputs();
        }

        virtual void _evaluate() {
            setOutput(this);

            // Read inputs
            readAllInputs();
        }

        double m_revLimit = 0.0;
        FunctionNode *m_timingCurve = nullptr;
        double m_limiterDuration = 0.0;
        double m_firingsPerCycle = 1;
        bool m_compressionIgnition = false;
        double m_maxFuelPerInjection = 0.0;
        double m_idleSpeed = 0.0;
        double m_governedSpeed = 0.0;
        double m_autoignitionTemperature = 0.0;
        std::vector<Post> m_posts;
    };

} /* namespace es_script */

#endif /* ATG_ENGINE_SIM_IGNITION_MODULE_NODE_H */
