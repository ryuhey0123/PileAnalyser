import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';

import "normalize.css";

import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css";
import "@blueprintjs/select/lib/css/blueprint-select.css";
import "@blueprintjs/table/lib/css/table.css";

import "react-datasheet/lib/react-datasheet.css";

import InputForm from "./InputForm";
import GroundData from "./groundData"
// import Datasheet from './Datasheet';
import Chart from './Chart';

const App = () => (
  <div>
    <h1>多層地盤中の杭の非線形解析</h1>
    <InputForm />
    <GroundData />
    {/* <Datasheet /> */}
    <Chart />
  </div>
);

ReactDOM.render(<App />, document.getElementById("root"));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
