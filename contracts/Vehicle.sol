pragma solidity ^0.5.0;

contract Vehicle {
  uint public vehicleCount = 0;

  struct Veh {
    uint vid;
    uint speed;
    int256 latitude;
    int256 longitude;
    bool isTwoWheeler;
  }

  mapping(uint => Veh) public vehicles;

  constructor() public {
    addVehicle(60, 821462.123, 1026429.456, true);
    addVehicle(20, 1621232.32, 1026429.34, false);
  }

  function addVehicle(uint speed, int256 latitude, int256 longitude, bool twoWheeler) public {
    vehicleCount++;
    vehicles[vehicleCount] = Veh(vehicleCount, speed, latitude, longitude, twoWheeler);
  }
}