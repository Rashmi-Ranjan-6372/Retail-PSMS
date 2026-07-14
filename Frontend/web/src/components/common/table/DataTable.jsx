import React from "react";
import { Table, Thead, Tbody, Tr, Th, Td, Box } from "@chakra-ui/react";

import {
  tableContainer,
  table,
  tableHeader,
  tableRow,
  tableCell,
  tableEmpty,
} from "../../../styles/components/table";

const DataTable = ({
  columns = [],
  data = [],
  emptyMessage = "No records found",
}) => {
  return (
    <Box sx={tableContainer}>
      <Table sx={table}>
        <Thead>
          <Tr>
            {columns.map((column) => (
              <Th key={column.accessor} sx={tableHeader}>
                {column.Header}
              </Th>
            ))}
          </Tr>
        </Thead>

        <Tbody>
          {data.length > 0 ? (
            data.map((row, index) => (
              <Tr key={index} sx={tableRow}>
                {columns.map((column) => (
                  <Td key={column.accessor} sx={tableCell}>
                    {column.Cell ? column.Cell(row) : row[column.accessor]}
                  </Td>
                ))}
              </Tr>
            ))
          ) : (
            <Tr>
              <Td colSpan={columns.length} sx={tableEmpty}>
                {emptyMessage}
              </Td>
            </Tr>
          )}
        </Tbody>
      </Table>
    </Box>
  );
};

export default DataTable;
