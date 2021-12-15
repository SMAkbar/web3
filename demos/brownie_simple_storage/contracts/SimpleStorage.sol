// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    // unit256 initialized to 0
    uint256 favoriteNumber;

    // new types
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // array dynamic array
    People[] public people;

    // mapping
    mapping(string => uint256) public nameToFavoriteNumber;

    // people
    People public person = People({favoriteNumber: 2, name: "Muhammad Akbar"});

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view function does not require transaction fee
    function retreive() public view returns (uint256) {
        return favoriteNumber;
    }

    // add person to an array
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
