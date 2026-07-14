import { Button } from "@chakra-ui/react";
import { outlineButton } from "../../../styles/components/buttons";

const OutlineButton = ({
  children,
  isLoading,
  loadingText,
  leftIcon,
  rightIcon,
  ...props
}) => {
  return (
    <Button
      sx={outlineButton}
      isLoading={isLoading}
      loadingText={loadingText}
      leftIcon={leftIcon}
      rightIcon={rightIcon}
      {...props}
    >
      {children}
    </Button>
  );
};

export default OutlineButton;
