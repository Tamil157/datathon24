import React, { useState, useEffect } from "react";
import './css/top.css';
import axios from "axios";
import Navbar from "./Nav";

export default function Top() {
    const [topUnitNames, setTopUnitNames] = useState([]);
    const [complaints, setComplaints] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await fetch('/top-unit-names');
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json();
                setTopUnitNames(data.top_unit_names);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        async function fetchComplaints() {
            try {
                const response = await axios.get('/complaints');
                setComplaints(response.data.complaints);
            } catch (error) {
                console.error('Error fetching complaints:', error);
            }
        }

        fetchData().then(fetchComplaints);
    }, []);

    // Filter complaints based on topUnitNames
    const peopleInRiskZone = complaints.filter(complaint => topUnitNames.includes(complaint.distname));
    console.log(peopleInRiskZone)
    return (
        <>
            <Navbar />
            <div className="accident-wrapper">
                <h2 className="h2-heading">Top 5 Unit Names:</h2>
                <ul>
                    {topUnitNames && topUnitNames.map((unitname, index) => (
                        <p className="city-name" key={index}>{unitname}</p>
                    ))}
                </ul>
            </div>
            <div className="accident-wrapper">
                <h2 className="h2-heading">People in Risk Zone:</h2>
                <ul>
                    {peopleInRiskZone && peopleInRiskZone.map((complaint, index) => (
                        <p className="city-name" key={index}>{complaint}</p>
                    ))}
                </ul>
            </div>
        </>
    );
}
