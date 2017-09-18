import React from 'react';
import Header from './header.jsx';
import ArchiveList from './archivelist.jsx'

class Main extends React.Component{
    render(){
        return(
            <div>
                <Header />
                <ArchiveList/>
            </div>
        )
    }
}

export default Main;