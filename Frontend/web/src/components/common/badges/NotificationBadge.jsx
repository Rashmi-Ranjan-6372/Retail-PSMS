import { Badge } from "@chakra-ui/react";
import { notificationBadge } from "../../../styles/components/badges";

const NotificationBadge = ({ count = 0, max = 99 }) => {
  if (!count) return null;

  return (
    <Badge sx={notificationBadge}>{count > max ? `${max}+` : count}</Badge>
  );
};

export default NotificationBadge;
