import { Box } from "@chakra-ui/react";

import Capsule from "../../assets/pharmacy-icons/capsule-medicine.svg";
import MedicineCross from "../../assets/pharmacy-icons/medical-cross.svg";
import Hospital from "../../assets/pharmacy-icons/hospital.svg";
import Pill from "../../assets/pharmacy-icons/pill.svg";
import Prescription from "../../assets/pharmacy-icons/prescription.svg";
import Stethoscope from "../../assets/pharmacy-icons/stethoscope.svg";
import Syringe from "../../assets/pharmacy-icons/syringe-medical.svg";
import Doctor from "../../assets/pharmacy-icons/doctor-man.svg";
import Monitor from "../../assets/pharmacy-icons/health-monitor.svg";
import HospitalLocation from "../../assets/pharmacy-icons/hospital-location.svg";
import PatientBed from "../../assets/pharmacy-icons/patient-bed.svg";
import Temperature from "../../assets/pharmacy-icons/temperature.svg";

import {
  pharmacyBackground,
  backgroundIcon,
  iconPositions,
} from "../../styles/common/layout";

const icons = [
  Capsule,
  MedicineCross,
  Hospital,
  Pill,
  Prescription,
  Stethoscope,
  Syringe,
  Doctor,
  Monitor,
  HospitalLocation,
  PatientBed,
  Temperature,
];

const Background = () => {
  return (
    <Box sx={pharmacyBackground}>
      {icons.map((icon, index) => (
        <Box
          key={index}
          as="img"
          src={icon}
          alt=""
          sx={{
            ...backgroundIcon,
            ...iconPositions[`icon${index + 1}`],
          }}
        />
      ))}
    </Box>
  );
};

export default Background;