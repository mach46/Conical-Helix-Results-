import os
import sys

diameter = sys.argv[1]
rpm = sys.argv[2]

# boundary names (IMPORTANT)
inlet_name  = "inlet"
outlet_name = "outlet"
wall_name   = "wall"

# output directory
base_path = "/scratch/24cr60r06/dhairya/data_files/session_files"
extracted_base = "/scratch/24cr60r06/dhairya/data_files/extracted_data"

statepoint_folder = os.path.join(base_path, "state_point_files")
statepoint_data_folder = os.path.join(extracted_base,"statepoint_data")

# File paths
cse_file = os.path.join(
    statepoint_folder,
    f"rotation_{diameter}_{rpm}_state_point.cse"
)
output_csv = os.path.join(
    statepoint_data_folder,
    f"rotation_{diameter}_{rpm}_state_point_data.csv"
)

# ============================
# WRITE CSE FILE
# ============================

with open(cse_file, "w") as f:

    f.write(f"""
COMMAND FILE:
  CFX Post Version = 23.2
END

!open(FILE, '> {output_csv}');
    
# ==============================
# HEADER
# ==============================
!print FILE "Pin,Tin,rhoin,muin,hin,sin,vin,Min,VThetain,P0in,T0in,htin,Pout,Tout,rhoout,muout,hout,sout,vout,Mout,VThetaout,P0out,T0out,htout,mdot,Fx,Fy,Fz,Tx,Ty,Tz,tau_w\\n";

# ==============================
# INLET (massFlowAve preferred)
# ==============================
! $Pin   = massFlowAve("Pressure","{inlet_name}");
! $Tin   = massFlowAve("Temperature","{inlet_name}");
! $rhoin = massFlowAve("Density","{inlet_name}");
! $muin = massFlowAve("Dynamic Viscosity","{inlet_name}");


! $hin   = massFlowAve("Static Enthalpy","{inlet_name}");
! $sin   = massFlowAve("Static Entropy","{inlet_name}");

! $vin   = massFlowAve("Velocity","{inlet_name}");
! $Min   = massFlowAve("Mach Number","{inlet_name}");
! $VThetain  = areaAve("Velocity Circumferential","{inlet_name}");

! $P0in  = massFlowAve("Total Pressure","{inlet_name}");
! $T0in  = massFlowAve("Total Temperature","{inlet_name}");
! $htin  = massFlowAve("Total Enthalpy","{inlet_name}");

# ==============================
# OUTLET
# ==============================
! $Pout   = massFlowAve("Pressure","{outlet_name}");
! $Tout   = massFlowAve("Temperature","{outlet_name}");
! $rhoout = massFlowAve("Density","{outlet_name}");
! $muout = massFlowAve("Dynamic Viscosity","{outlet_name}");


! $hout   = massFlowAve("Static Enthalpy","{outlet_name}");
! $sout   = massFlowAve("Static Entropy","{outlet_name}");

! $vout   = massFlowAve("Velocity","{outlet_name}");
! $Mout   = massFlowAve("Mach Number","{outlet_name}");
! $VThetaout  = areaAve("Velocity Circumferential","{outlet_name}");

! $P0out  = massFlowAve("Total Pressure","{outlet_name}");
! $T0out  = massFlowAve("Total Temperature","{outlet_name}");
! $htout  = massFlowAve("Total Enthalpy","{outlet_name}");

# ==============================
# MASS FLOW
# ==============================
! $mdot = massFlow("{outlet_name}");

# ==============================
# FORCES
# ==============================
! $Fx = force("{wall_name}","X");
! $Fy = force("{wall_name}","Y");
! $Fz = force("{wall_name}","Z");

# ==============================
# TORQUES
# ==============================
! $Tx = torque("{wall_name}","X");
! $Ty = torque("{wall_name}","Y");
! $Tz = torque("{wall_name}","Z");

# ==============================
# WALL SHEAR STRESS
# ==============================
! $tau_w = areaAve("Wall Shear","{wall_name}");

# ==============================
# PRINT
# ==============================
!print FILE "$Pin,$Tin,$rhoin,$muin,$hin,$sin,$vin,$Min,$VThetain,$P0in,$T0in,$htin,$Pout,$Tout,$rhoout,$muout,$hout,$sout,$vout,$Mout,$VThetaout,$P0out,$T0out,$htout,$mdot,$Fx,$Fy,$Fz,$Tx,$Ty,$Tz,$tau_w\\n";

!close(FILE);
""")

    print(f"Full CSE script generated   → {cse_file}")
