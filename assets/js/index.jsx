import React from 'react';
import ReactDOM from 'react-dom';
import ArchiveList from './apps/archivelist'
import RecordList from './apps/recordlist'

class Main extends React.Component{
    render(){
        return(
            <div>
                <RecordList/>
            </div>
        )
    }
}


ReactDOM.render(<Main/>, document.getElementById('container'))