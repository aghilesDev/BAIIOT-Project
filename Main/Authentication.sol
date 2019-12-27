        pragma solidity 0.4.25;
contract Authentication {

    address owner;
    mapping (address => bool) public users;
    mapping (address => Iot) public iots;
    mapping (address => bool) public servers;



    struct Iot{
        bool val;
        string ip;


    }


    constructor () public{
        owner=msg.sender;
    }




    function addUser(address user) public returns(bool){
        if(msg.sender != owner) return false;
        users[user]=true;
        return users[user];
    }

    function addIot(address iotAddress,string memory ip) public returns(bool){
        if(msg.sender != owner) return false;
        Iot memory iot;
        iot.val=true;
        iot.ip=ip;
        iots[iotAddress]=iot;
        return true;
        }

        function addServer(address server) public returns(bool){
        if(msg.sender != owner) return false;
        servers[server]=true;
        return servers[server];
        }

        function userIsPermited(address user) view public returns(bool){

            return users[user];
        }



        function ServerIsPermited(address server) view public returns(bool){
            return servers[server];
        }



        function iotIsPermited(address iotAddress) view public returns(bool){
            if(iots[iotAddress].val==true)
                return (true);
            else
                return false;
        }



    function setOwner(address newOwner) public{
        if(msg.sender != owner) return;
        owner=newOwner;
    }
}
