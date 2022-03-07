// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public usdEntryFee;
    uint256 public randomness;

    AggregatorV3Interface internal ethUSDPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSE,
        CACLUCATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUSDPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSE;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // $50 min
        // require(condition);
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough Fee");
        players.push(msg.sender);
    }

    function startLottery() public {
        require(
            lottery_state == LOTTERY_STATE.CLOSE,
            "can't start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // uint256(
        //     keccack256(
        //         abi.encodePacked(
        //             nonce, // predictable
        //             msg.sender, // predictable
        //             block.difficulty, // can actually be manipulated by the miners!
        //             block.timestamp // predictable
        //         )
        //     )
        // ) % players.length;
        lottery_state = LOTTERY_STATE.CACLUCATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CACLUCATING_WINNER,
            "You aren't there yet"
        );
        require(_randomness > 0, "random-not-found");

        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        randomness = _randomness;

        // Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSE;
    }

    /**
     * Returns the latest price
     */
    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUSDPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }
}
