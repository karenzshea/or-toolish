from __future__ import print_function
import sys
from ortools.constraint_solver.pywrapcp import RoutingModel


def printAssignment(assignment, model):
    capacityDimension = model.GetDimensionOrDie('Capacity')
    timeDimension = model.GetDimensionOrDie('Time')

    route = []
    node = model.Start(0)

    while not model.IsEnd(node):
        loadVar = capacityDimension.CumulVar(node)
        timeVar = timeDimension.CumulVar(node)

        route.append({'node': node,
                      'load': assignment.Value(loadVar),
                      'time': [assignment.Min(timeVar), assignment.Max(timeVar)]})

        node = assignment.Value(model.NextVar(node))

    print(route)


def main():
    numLocations = 8
    depotIndex = 0
    numVehicles = 3
    vehicleCapacity = 3

    times =[ [ 0, 957.7, 748.5, 570.8, 706.7, 574.2, 893.2, 187 ],
           [ 975.1, 0, 436.6, 894.6, 293, 446.4, 760.2, 901.2 ],
           [ 814.6, 399.6, 0, 458, 352.5, 231.5, 876.8, 675.8 ],
           [ 526.8, 841.3, 441.7, 0, 785.8, 598.5, 1266.5, 457.8 ],
           [ 733.3, 328.4, 351.6, 748.7, 0, 231.8, 625, 659.4 ],
           [ 713.7, 360.9, 174.3, 577.1, 270.3, 0, 845.2, 639.8 ],
           [ 917.6, 919.7, 1000.8, 1357.9, 733.1, 931, 0, 996.4 ],
           [ 246.7, 901.6, 626.4, 383.8, 673.9, 540.7, 986.4, 0 ] ]


    def timeCallback(s, t):
        return times[s][t]

    #demands = [0, 0, 1, 1, 3, 0, 0, 1]
    demands = [0, 1, 1, 1, 1, 1, 1, 1]

    def demandsCallback(s, _):
        return demands[s];

    pickupDeliveries = [(6,4), (5,4)] #[ ( 6, 4 ), ( 5, 4 ), ( 5, 3 ), ( 1, 2 ), ( 5, 2 ), ( 6, 4 ), ( 5, 7 ) ];
    model = RoutingModel(numLocations, numVehicles, depotIndex)
    model.SetArcCostEvaluatorOfAllVehicles(timeCallback);

    model.AddDimension(timeCallback, 28800, 28800, True, 'Time')
    timeDimension = model.GetDimensionOrDie('Time');
    for i in range(numLocations):
        timeDimension.CumulVar(i).SetRange(0, 28800)

    model.AddDimension(demandsCallback, 0, vehicleCapacity, True, 'Capacity')
    capacityDimension = model.GetDimensionOrDie('Capacity');

    solver = model.solver()

    for pickup, delivery in pickupDeliveries:
        pickupIndex = model.NodeToIndex(pickup)
        deliveryIndex = model.NodeToIndex(delivery)

        solver.AddConstraint(model.VehicleVar(pickupIndex) == model.VehicleVar(deliveryIndex))
        solver.AddConstraint(timeDimension.CumulVar(pickupIndex) <= timeDimension.CumulVar(deliveryIndex))

        model.AddPickupAndDelivery(pickup, delivery)


    assignment = model.Solve()

    if not assignment:
        sys.exit('Error: No Assignment')

    printAssignment(assignment, model)


if __name__ == '__main__':
    main()
