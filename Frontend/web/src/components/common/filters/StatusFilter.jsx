import SelectInput from "../inputs/SelectInput";

import { statusFilter } from "../../../styles/components/filters";

const StatusFilter = ({
  value,
  onChange,
  options = [
    { value: "", label: "All Status" },
    { value: "active", label: "Active" },
    { value: "inactive", label: "Inactive" },
  ],
  ...props
}) => {
  return (
    <SelectInput sx={statusFilter} value={value} onChange={onChange} {...props}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </SelectInput>
  );
};

export default StatusFilter;
