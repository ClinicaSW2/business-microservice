-- Drop existing reservacion table if it exists
DROP TABLE IF EXISTS reservacion;

-- Create reservacion table with all required fields
CREATE TABLE reservacion (
    id serial,
    doctor_name VARCHAR(100),
    especialidad VARCHAR(50),
    paciente_name VARCHAR(100),
    paciente_last_name VARCHAR(100),
    paciente_address VARCHAR(200),
    paciente_sexo CHAR(1),
    fecha_reservado DATE,
    fecha_cancelado DATE,
	fecha_atendido DATE,
    stado_state VARCHAR(30),
    cantidad INT,
    tiempo_atencion INT,
    cantida_anticipacion INT,
    costo FLOAT
);

CREATE OR REPLACE PROCEDURE GenerateRandomData()
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
    doctor_names VARCHAR(20)[20];
    especialidad VARCHAR(30)[12];
	precio int[12];
    paciente_names VARCHAR(15)[15];
    paciente_last_names VARCHAR(20)[20];
    stado_states VARCHAR(20)[10];
    sexos CHAR(2)[3];
	random int;
	fecha_reservado date;
	fecha_atendido date;
BEGIN
    doctor_names := ARRAY['Dr. John Smith', 'Dr. Jane Doe', 'Dr. Albert Johnson', 'Dr. Mary Brown', 'Dr. Chris Lee', 'Dr. Pat Taylor', 'Dr. Alex Martinez', 'Dr. Sam Wilson', 'Dr. Lee Anderson', 'Dr. Kim Thomas', 'Dr. Mark Harris', 'Dr. Laura Clark', 'Dr. Susan Young', 'Dr. Paul Allen', 'Dr. Rita King', 'Dr. Olivia Scott', 'Dr. Henry Moore', 'Dr. Carol Turner', 'Dr. Peter Wright', 'Dr. Linda Hill'];
    especialidad := ARRAY['Oftalmólogo','Oftalmólogo','Oftalmólogo','Oftalmólogo', 'Optometrista','Optometrista','Optometrista','Óptico','Óptico', 'Óptico', 'Oftalmólogo pediátrico', 'Cirujano oftalmólogo'];
    precio := ARRAy[50,50,50,50,65,65,65,70,70,70,75,80];
	paciente_names := ARRAY['Emily', 'Michael', 'Sarah', 'David', 'Sophia', 'James', 'Isabella', 'William', 'Mia', 'Benjamin', 'Charlotte', 'Lucas', 'Amelia', 'Alexander', 'Harper'];
    paciente_last_names := ARRAY['Clark', 'Brown', 'Davis', 'Martinez', 'Miller', 'Wilson', 'Taylor', 'Anderson', 'Thomas', 'Harris', 'Moore', 'Young', 'Allen', 'King', 'Scott', 'Turner', 'Wright', 'Hill', 'Lewis', 'Walker'];
    stado_states := ARRAY['Excelente','Excelente','Excelente','Excelente','Buena', 'Buena',  'Buena', 'Promedio', 'Mala', 'Pesima'];
    sexos := ARRAY['M','M', 'F'];

    WHILE i <= 5000 LOOP
	
	random := FLOOR(1 + RANDOM() * 12);
	fecha_reservado :='2019-01-01'::DATE + (FLOOR(RANDOM() * 1825)) * INTERVAL '1 day';
	fecha_atendido :=fecha_reservado::DATE + (FLOOR(RANDOM() * 5)) * INTERVAL '1 day';
	
        INSERT INTO reservacion (
            doctor_name, especialidad, paciente_name, paciente_last_name, paciente_address, paciente_sexo, fecha_reservado, fecha_cancelado,fecha_atendido, stado_state, cantidad, tiempo_atencion, cantida_anticipacion, costo
        ) VALUES (
            doctor_names[FLOOR(1 + RANDOM() * 20)],
            especialidad[random],
            paciente_names[FLOOR(1 + RANDOM() * 15)],
            paciente_last_names[FLOOR(1 + RANDOM() * 20)],
            CONCAT(FLOOR(1 + RANDOM() * 9999), ' ', paciente_last_names[FLOOR(1 + RANDOM() * 20)], ' Street'),
            sexos[FLOOR(1 + RANDOM() * 3)],
            fecha_reservado,
            CASE WHEN RANDOM() < 0.1 THEN fecha_atendido::DATE - (FLOOR(RANDOM() * 3)) * INTERVAL '1 day' ELSE NULL END,
            fecha_atendido,
			stado_states[FLOOR(1 + RANDOM() * 10)],
            1,
            FLOOR(10 + RANDOM() * 25),
            FLOOR(1 + RANDOM() * 30),
            precio[random]-- Redondear a dos decimales
        );
        i := i + 1;
    END LOOP;
END $$;

call GenerateRandomData();
select *from reservacion