import React from 'react';

const Transaction = props => {
    return(
        <div className="transaction">
            <p>Block Number = {props.transaction.index}</p>
            <p>Sender = {props.transaction.sender}</p>
            <p>Recipient = {props.transaction.recipient}</p>
            <p>Amount = {props.transaction.amount}</p>
        </div>
    )
}

export default Transaction;