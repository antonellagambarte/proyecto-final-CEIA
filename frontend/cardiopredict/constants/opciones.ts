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
  DIARIAMENTE: 10,
  CASI_DIARIO: 9,
  TRES_CUATRO_SEMANA: 8,
  DOS_VECES_SEMANA: 7,
  UNA_VEZ_SEMANA: 6,
  DOS_TRES_MES: 5,
  UNA_VEZ_MES: 4,
  SIETE_ONCE_AÑO: 3,
  TRES_SEIS_AÑO: 2,
  UNA_DOS_AÑO: 1,
};

export const OpcionesAnhedonia = {
  NADA: 0,
  VARIOS_DIAS: 1,
  MAS_DE_LA_MITAD: 2,
  CASI_TODOS: 3,
} as const;
