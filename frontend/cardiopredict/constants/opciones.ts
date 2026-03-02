// types/paciente.ts

export const Sexo = {
  MACULINO: "M",
  FEMENINO: "F",
};

export const OpcionesBinarias = {
  SI: "S",
  NO: "N",
};

export const OpcionesCompletas = {
  ...OpcionesBinarias,
  NO_SABE: "X",
};

export const OpcionesDiabetes = {
  ...OpcionesBinarias,
  NO_SABE: "X",
  PREDIABETES: "P",
};

export const OpcionesAlcohol = {
  NUNCA: 0,
  DIARIAMENTE: 1,
  CASI_DIARIO: 2,
  TRES_CUATRO_SEMANA: 3,
  DOS_VECES_SEMANA: 4,
  UNA_VEZ_SEMANA: 5,
  DOS_TRES_MES: 6,
  UNA_VEZ_MES: 7,
  SIETE_ONCE_AÑO: 8,
  TRES_SEIS_AÑO: 9,
  UNA_DOS_AÑO: 10,
  NO_SABE: 99,
};

export const OpcionesAnhedonia = {
  NADA: 0,
  VARIOS_DIAS: 1,
  MAS_DE_LA_MITAD: 2,
  CASI_TODOS: 3,
  NO_SABE: 9,
} as const;
