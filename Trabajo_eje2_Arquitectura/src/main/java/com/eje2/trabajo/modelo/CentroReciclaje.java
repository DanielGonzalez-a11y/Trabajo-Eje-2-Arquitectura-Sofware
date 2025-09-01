package com.eje2.trabajo.modelo;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import jakarta.persistence.*;
import com.eje2.trabajo.modelo.CentroMaterial;

@Entity
@Table(name = "centros_reciclaje")
public class CentroReciclaje {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_centro;

    private String nombre_centro;
    private String direccion;
    private String telefono;
    private String horario_atencion;
    private BigDecimal latitud;
    private BigDecimal longitud;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @OneToMany(mappedBy = "centro", cascade = CascadeType.ALL)
    private List<CentroMaterial> materiales;

	public Long getId_centro() {
		return id_centro;
	}

	public void setId_centro(Long id_centro) {
		this.id_centro = id_centro;
	}

	public String getNombre_centro() {
		return nombre_centro;
	}

	public void setNombre_centro(String nombre_centro) {
		this.nombre_centro = nombre_centro;
	}

	public String getDireccion() {
		return direccion;
	}

	public void setDireccion(String direccion) {
		this.direccion = direccion;
	}

	public String getTelefono() {
		return telefono;
	}

	public void setTelefono(String telefono) {
		this.telefono = telefono;
	}

	public String getHorario_atencion() {
		return horario_atencion;
	}

	public void setHorario_atencion(String horario_atencion) {
		this.horario_atencion = horario_atencion;
	}

	public BigDecimal getLatitud() {
		return latitud;
	}

	public void setLatitud(BigDecimal latitud) {
		this.latitud = latitud;
	}

	public BigDecimal getLongitud() {
		return longitud;
	}

	public void setLongitud(BigDecimal longitud) {
		this.longitud = longitud;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}

	public List<CentroMaterial> getMateriales() {
		return materiales;
	}

	public void setMateriales(List<CentroMaterial> materiales) {
		this.materiales = materiales;
	}
    
}
