import { IconButton as ChakraIconButton } from "@chakra-ui/react";
import { iconButton } from "../../../styles/components/buttons";

const IconButton = ({
  icon,
  "aria-label": ariaLabel = "icon-button",
  ...props
}) => {
  return (
    <ChakraIconButton
      sx={iconButton}
      icon={icon}
      aria-label={ariaLabel}
      {...props}
    />
  );
};

export default IconButton;
