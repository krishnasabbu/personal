                    Organization
                         │
                    owns/manages
                         │
                       Team
                         │
                  ownsApplication
                         │
                   Application
                         │
                hasDeployment
                         │
                 DeploymentUnit
                         │
                      runsOn
                         │
                 Compute Resource
           ┌─────────────┼──────────────┐
           │             │              │
          VM       Kubernetes Pod    Container
           │             │
        hostedIn     scheduledOn
           │             │
        Cluster      Kubernetes Node
              │
          locatedIn
              │
            Zone
              │
          locatedIn
              │
         Datacenter
              │
          belongsTo
              │
           Region
              │
         belongsTo
              │
        Cloud Provider