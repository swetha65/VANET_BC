pragma solidity 0.8.0;

contract ContactList {
    struct Contact {
        string name;
        string phoneNumber;
    }

    Contact[] public contacts;
    mapping(string => string) public nameToPhoneNumber;
    mapping(string => uint256) public contactIndex;

    function retrieve() public view returns (Contact[] memory) {
        return contacts;
    }

    function addContact(string memory _name, string memory _phoneNumber) public {
        contacts.push(Contact(_name, _phoneNumber));
        nameToPhoneNumber[_name] = _phoneNumber;
        contactIndex[_name] = contacts.length - 1;
    }

    function removeContact(uint256 contact_id) public {
        require(contact_id < contacts.length, "Invalid contact ID");

        Contact storage contactToRemove = contacts[contact_id];
        string memory nameToRemove = contactToRemove.name;

        // Swap the contact to be removed with the last contact in the array
        contacts[contact_id] = contacts[contacts.length - 1];
        contactIndex[contacts[contact_id].name] = contact_id;

        // Delete the last element in the array
        contacts.pop();

        // Clear the mappings for the removed contact
        delete nameToPhoneNumber[nameToRemove];
        delete contactIndex[nameToRemove];
    }
}
