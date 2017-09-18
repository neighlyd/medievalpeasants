import React from 'react';
import axios from 'axios';


class ArchiveList extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            archives:[]
        };
    }

    // Use axios to obtain data from API and append to state.
    componentDidMount(){
        console.log("Sending axios API request");
        console.log(this.state);
        axios.get("/api/archives")
            .then(res => {
            console.log("Received axios API request");
            console.log(res.data);
            this.setState({archives: res.data});
            console.log(this.state);
        })
            .catch(function(error){
                console.log(error);
        });
    }

    // render state to DOM, using map function to tie array's key to values for list.
    render(){
        return (
                <ul>
                    {this.state.archives.map(archives =>
                        <li key={archives.id}>
                            Name: {archives.name}<br/>
                            Website: <a href={archives.website}>Link</a><br/>
                            Notes: {archives.notes}
                        </li>
                    )}
                </ul>
        );
    }
}


export default ArchiveList