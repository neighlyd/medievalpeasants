import React from 'react';
import axios from 'axios';


class RecordList extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            records:[]
        };
    }



    componentDidMount(){
        console.log("Sending axios API request");
        console.log(this.state);
        axios.get("/api/records")
            .then(res => {
            console.log("Received axios API request");
            console.log(res.data);
            this.setState({records: res.data});
            console.log(this.state);
        })
            .catch(function(error){
                console.log(error);
        });
    }


    render(){
        return (
                <ul>
                    {this.state.records.map(records =>
                        <li key={records.id}>
                            Record Name: {records.name}<br/>
                            Archive Name: {records.archive.name}<br/>
                            Record Type: {records.record_type}<br/>
                            Reel Number: {records.reel}<br/>
                            Notes: {records.notes.split(/[\n\r]+/).map((item, text) => {
                            return <span break={text}>{item}<br/></span>
                        })}
                        <br/>
                        </li>
                    )}
                </ul>
        );
    }
}


export default RecordList