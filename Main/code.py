    with open("KeyContract","w") as file:
        file.write(json.dumps(self.contract_interface['abi']))
    with open("KeyContract","r") as file2:
        val=file2.read()
        val=json.loads(val)
        print(val)
