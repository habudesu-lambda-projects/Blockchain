import React, {useState} from 'react';
import './App.css';
import axios from 'axios';
import Transaction from './Transaction';

function App() {

  const [transactions, setTransactions] = useState([])
  const [user, setUser] = useState("")
  const [balance, setBalance] = useState(0)

  const getTransactions = user => {
    axios.get('http://localhost:5000/chain', {headers: {"Content-Type": 'application/json'}})
      .then(res => {
        setBalance(0)
        let transactionList = []
        res.data.chain.forEach(block => {
          console.log(block)
          transactionList = [...transactionList, ...block.transactions]
        })
        let userTransactions = transactionList.filter(transaction => transaction.recipient == user || transaction.sender == user)
        setTransactions(userTransactions)
        let userBalance = 0
        userTransactions.forEach(transaction => {
          if(transaction.sender === user) {
            userBalance += transaction.amount
          }
          if(transaction.recipient === user) {
            userBalance += transaction.amount
          }
        })
        setBalance(userBalance)
      })
      .catch(err => console.log(err))
  }

  const handleChange = event => {
    setUser(event.target.value)
  }

  return (
    <div className="App">
      <label>User</label>
      <input onChange={handleChange} placeholder="user"/>
      <button onClick={() => getTransactions(user)}>Get Transactions</button>
      <p>User Balance: {balance}</p>
      {transactions.length === 0 ?
        <p>No Transactions</p> :
        transactions.map(transaction => <Transaction transaction={transaction}/>)
      }
    </div>
  )
}

export default App;
