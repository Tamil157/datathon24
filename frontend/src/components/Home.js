import React from 'react';
import mainHome from './css/mainHome.css'

const Home = () => {
    return (
        <>
            <main className='welcome-container'>
                <h1 className='welcome-head'>WELCOME TO ROADSAFE KARNATAKA</h1>
                <div className='animate-container'>
                    <p className='head-content'>Empowering Safer Roads through Data Analysis..</p>
                </div>               
                <p className='mission'>Join us in our mission to make Karnataka's roads safer. Whether you're a concerned citizen, a policymaker, or a member of law enforcement, together, we can make a difference.</p>
                <button className='user-btn'><a className='user-link' href='/submitcomplaint'>USER</a></button>
                <button className='admin-btn'><a className='admin-link' href='/login'>ADMIN</a></button> 
            </main>
            <footer className='aboutus-wrapper'>
                <hr></hr>
                <div>
                    <h3 className='aboutus'>About US</h3>
                    <p className='aboutus-content'>RoadSafe Karnataka is an initiative by the Karnataka Police aimed at leveraging data analytics to predict and prevent road accidents across the state. Our platform provides insights into various road types and identifies potential risk factors to enhance road safety measures.</p>
                </div> 
            </footer>
            
        </>
    );
};

export default Home;
