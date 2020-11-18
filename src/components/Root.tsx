import React, { useContext } from 'react';
import Context from '../Context';
import Chart from './Chart';

import GroundData from './GroundData';
import InputForm from './InputForm';

const Root = () => {

    const {state} = useContext(Context)

    return (
        <div>
            <InputForm/>
            <GroundData/>
            <Chart output={state.outputs.results}/>
        </div>
    );
};

export default Root;
