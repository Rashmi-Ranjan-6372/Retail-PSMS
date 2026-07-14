import { Badge } from "@chakra-ui/react";

import {
  activeBadge,
  inactiveBadge,
  successBadge,
  dangerBadge,
  warningBadge,
  infoBadge,
} from "../../../styles/components/badges";

const statusStyles = {
  active: activeBadge,
  inactive: inactiveBadge,
  success: successBadge,
  error: dangerBadge,
  danger: dangerBadge,
  warning: warningBadge,
  info: infoBadge,
};

const StatusBadge = ({ status = "", children }) => {
  const value = String(status).toLowerCase();

  return (
    <Badge sx={statusStyles[value] || infoBadge}>{children || status}</Badge>
  );
};

export default StatusBadge;
