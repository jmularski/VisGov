import React from 'react'; 
import axios from 'axios';

const{API_KEY}=process.env
const API_URL= 'https://micro.arria.com/services/rest/english/aOrAn?word=university&apikey=493F438D70561E97'

export class Search extends React.Component {

   state={
     query:'',
     results:[]

   }

   getInfo = () => {
    axios.get(`${API_URL}word=${this.state.query}&api_key=${API_KEY}`)
      .then(({ data }) => {
        this.setState({
          results: data.data                           
        })
      })
  }

   handleInputChange=()=>{
     this.setState({
       query:this.search.value
     })
   }


    render() {
      return (
        <form>
          <input
            placeholder="Search for a party..."
            ref={input=>this.search=input}
            onChange={this.handleInputChange}
          />
          <p>{this.state.query}</p>
        </form>
       
  
      );
    }
  }
  
 