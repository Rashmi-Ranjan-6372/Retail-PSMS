import { Skeleton } from "@chakra-ui/react";
import { skeleton } from "../../../styles/components/loaders";

const SkeletonLoader = ({ height = "20px", width = "100%", ...props }) => {
  return <Skeleton height={height} width={width} sx={skeleton} {...props} />;
};

export default SkeletonLoader;
