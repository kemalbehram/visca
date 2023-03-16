import pytest

from .utils import (
    ADDRS,
    CONTRACTS,
    KEYS,
    deploy_contract,
    send_transaction,
    w3_wait_for_new_blocks,
)


def test_gas_eth_tx(geth, visca):
    tx_value = 10

    # send a transaction with geth
    geth_gas_price = geth.w3.eth.gas_price
    tx = {"to": ADDRS["community"], "value": tx_value, "gasPrice": geth_gas_price}
    geth_receipt = send_transaction(geth.w3, tx, KEYS["validator"])

    # send an equivalent transaction with visca
    visca_gas_price = visca.w3.eth.gas_price
    tx = {"to": ADDRS["community"], "value": tx_value, "gasPrice": visca_gas_price}
    visca_receipt = send_transaction(visca.w3, tx, KEYS["validator"])

    # ensure that the gasUsed is equivalent
    assert geth_receipt.gasUsed == visca_receipt.gasUsed


def test_gas_deployment(geth, visca):
    # deploy an identical contract on geth and visca
    # ensure that the gasUsed is equivalent
    _, geth_contract_receipt = deploy_contract(geth.w3, CONTRACTS["TestERC20A"])
    _, visca_contract_receipt = deploy_contract(
        visca.w3, CONTRACTS["TestERC20A"]
    )
    assert geth_contract_receipt.gasUsed == visca_contract_receipt.gasUsed


def test_gas_call(geth, visca):
    function_input = 10

    # deploy an identical contract on geth and visca
    # ensure that the contract has a function which consumes non-trivial gas
    geth_contract, _ = deploy_contract(geth.w3, CONTRACTS["BurnGas"])
    visca_contract, _ = deploy_contract(visca.w3, CONTRACTS["BurnGas"])

    # call the contract and get tx receipt for geth
    geth_gas_price = geth.w3.eth.gas_price
    geth_txhash = geth_contract.functions.burnGas(function_input).transact(
        {"from": ADDRS["validator"], "gasPrice": geth_gas_price}
    )
    geth_call_receipt = geth.w3.eth.wait_for_transaction_receipt(geth_txhash)

    # repeat the above for visca
    visca_gas_price = visca.w3.eth.gas_price
    visca_txhash = visca_contract.functions.burnGas(function_input).transact(
        {"from": ADDRS["validator"], "gasPrice": visca_gas_price}
    )
    visca_call_receipt = visca.w3.eth.wait_for_transaction_receipt(
        visca_txhash
    )

    # ensure that the gasUsed is equivalent
    assert geth_call_receipt.gasUsed == visca_call_receipt.gasUsed


def test_block_gas_limit(visca):
    tx_value = 10

    # get the block gas limit from the latest block
    w3_wait_for_new_blocks(visca.w3, 5)
    block = visca.w3.eth.get_block("latest")
    exceeded_gas_limit = block.gasLimit + 100

    # send a transaction exceeding the block gas limit
    visca_gas_price = visca.w3.eth.gas_price
    tx = {
        "to": ADDRS["community"],
        "value": tx_value,
        "gas": exceeded_gas_limit,
        "gasPrice": visca_gas_price,
    }

    # expect an error due to the block gas limit
    with pytest.raises(Exception):
        send_transaction(visca.w3, tx, KEYS["validator"])

    # deploy a contract on visca
    visca_contract, _ = deploy_contract(visca.w3, CONTRACTS["BurnGas"])

    # expect an error on contract call due to block gas limit
    with pytest.raises(Exception):
        visca_txhash = visca_contract.functions.burnGas(
            exceeded_gas_limit
        ).transact(
            {
                "from": ADDRS["validator"],
                "gas": exceeded_gas_limit,
                "gasPrice": visca_gas_price,
            }
        )
        (visca.w3.eth.wait_for_transaction_receipt(visca_txhash))

    return
