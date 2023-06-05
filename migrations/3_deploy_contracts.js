var Vehicle = artifacts.require("./Vehicle.sol");

module.exports = function(deployer) {
  deployer.deploy(Vehicle);
};