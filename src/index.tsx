import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';

import "normalize.css";

import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css";
import "@blueprintjs/select/lib/css/blueprint-select.css";
import "@blueprintjs/table/lib/css/table.css";

import "./index.scss"

import InputForm from "./InputForm";
import { EditableTable } from "./EditableTable"
// import InputToChart from './InputToChart';

const App = () => (
  <div className="main">
    <h1>多層地盤中の杭の非線形解析</h1>
    <div className="contents">
      <section className="col-1">
        <InputForm />
      </section>
      <section className="col-2">
        <EditableTable />
      </section>
    </div>
    <div className="chart-contents">
      {/* <InputToChart props={""}/> */}
    </div>
  </div>
);

ReactDOM.render(<App />, document.getElementById("root"));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
