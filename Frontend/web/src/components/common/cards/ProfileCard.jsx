import { Box } from "@chakra-ui/react";
import { profileCard } from "../../../styles/components/cards";

const ProfileCard = ({ children, ...props }) => {
  return (
    <Box sx={profileCard} {...props}>
      {children}
    </Box>
  );
};

export default ProfileCard;
