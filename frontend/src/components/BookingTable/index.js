import React, { useState } from 'react';
import styled from 'styled-components';

const Table = styled.div`
    float: left;
`

const Column = styled.div`
    float: left;
`

function BookingTable(props) {

    const seats = [];
    const column_list = [];
    const per_column_list = [];
    for (var i = parseInt(props.start_range); i <= parseInt(props.end_range); i++) { seats.push(i); };
    for (var i = 0; i < parseInt(props.columns); i++) { column_list.push(i); };
    for (var i = 0; i < ( (parseInt(props.end_range)-parseInt(props.start_range))/parseInt(props.columns) ); i++) { per_column_list.push(i); };

    return (
        <Table>
            {column_list.map(function(object, i){
                return per_column_list.map(function(seat_object, x){
                    return <p column={i} key={x} >{x}</p>;
                })
            })}
        </Table>
    )
}

export default BookingTable;