import React from 'react';
import Chart from './Chart';

import GroundData from './GroundData';
import InputForm from './InputForm';

const Root = () => {

    return (
        <div>
            <InputForm/>
            <GroundData/>
            <Chart/>
        </div>
    );
};

export default Root;
