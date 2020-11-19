import React from 'react';
import Chart from './Chart';

import InputForm from './InputForm';
import { EditableTable } from './EditableTable';

const Root = () => {

    return (
        <div className="main">
            <h1>多層地盤中の杭の非線形解析</h1>
            <div className="contents">
                <section className="col-1">
                    <InputForm/>
                </section>
                <section className="col-2">
                    <EditableTable/>
                </section>
            </div>
            <Chart/>
        </div>
    );
};

export default Root;
