// import { type } from "os";
import React, { useState } from "react";
import { WidthProvider, Responsive, Layout } from "react-grid-layout";

import InputForm from "./InputForm";
import { EditableTable } from "./EditableTable"

interface IState {
    currentBreakpoint: string,
    compactType: "horizontal" | "vertical",
    mounted: boolean,
    layouts: {[key: string]: Layout[]}
}

const ResponsiveLocalStorageLayout: React.FunctionComponent<{props: any}> = ({ props }) => {
    const ResponsiveReactGridLayout = WidthProvider(Responsive);

    const [state] = useState<IState>({
        currentBreakpoint: "lg",
        compactType: "vertical",
        mounted: true,
        layouts: { lg: [
            {x: 0, y: 0, w: 2, h: 5, i: "0", static: true},
            {x: 2, y: 0, w: 10, h: 5, i: "1", static: true},
            {x: 0, y: 5, w: 12, h: 5, i: "2", static: true},
        ] }
    })

    return (
        <div>
            <ResponsiveReactGridLayout
                {...props}
                layouts={state.layouts}
                // onBreakpointChange={this.onBreakpointChange}
                // onLayoutChange={this.onLayoutChange}
                // onDrop={this.onDrop}
                // WidthProvider option
                measureBeforeMount={false}
                // I like to have it animate on mount. If you don't, delete `useCSSTransforms` (it's default `true`)
                // and set `measureBeforeMount={true}`.
                useCSSTransforms={state.mounted}
                compactType={state.compactType}
                preventCollision={!state.compactType}
            >
                <div key="0" style={{ border: 1, borderStyle: "solid" }}><InputForm/></div>
                <div key="1" style={{ border: 1, borderStyle: "solid" }}><EditableTable/></div>
                <div key="2" style={{ border: 1, borderStyle: "solid" }}></div>
            </ResponsiveReactGridLayout>
        </div>
    )
}

export default ResponsiveLocalStorageLayout;
