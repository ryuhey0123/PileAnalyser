import React from 'react';
import Chart from './chart';

import InputForm from './inputForm';
import SoildataTable from './soilTable';

const Root = () => {

    return (
        <div className="main">
            <h1>多層地盤中の杭の非線形解析</h1>
            <div className="contents">
                <section className="col-1">
                    <InputForm/>
                </section>
                <section className="col-2">
                    <Chart/>
                </section>
            </div>
            <div className="contents">
                <SoildataTable/>
            </div>
        </div>
    );
};

export default Root;
