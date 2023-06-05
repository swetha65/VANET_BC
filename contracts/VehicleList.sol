pragma solidity 0.8.0;

contract VehicleList {
    struct Vehicle {
        uint256 vid;
        uint256 speed;
        string model;
        string color;
    }

    Vehicle[] public vehicles;
    mapping(uint256 => uint256) public vehicleIndex;

    function retrieve() public view returns (Vehicle[] memory) {
        return vehicles;
    }

    function addVehicle(uint256 _vid, uint256 _speed, string memory _model, string memory _color) public {
        vehicles.push(Vehicle(_vid, _speed, _model, _color));
        vehicleIndex[_vid] = vehicles.length - 1;
    }

    function removeVehicle(uint256 _vid) public {
        require(_vid > 0 && _vid <= vehicles.length, "Invalid vehicle ID");

        uint256 indexToRemove = vehicleIndex[_vid];
        uint256 lastIndex = vehicles.length - 1;

        // Swap the vehicle to be removed with the last vehicle in the array
        vehicles[indexToRemove] = vehicles[lastIndex];
        vehicleIndex[vehicles[lastIndex].vid] = indexToRemove;

        // Delete the last element in the array
        vehicles.pop();

        // Clear the mapping for the removed vehicle
        delete vehicleIndex[_vid];
    }
}