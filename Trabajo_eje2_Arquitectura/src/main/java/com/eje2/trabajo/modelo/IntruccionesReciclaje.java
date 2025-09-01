package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import com.eje2.trabajo.modelo.TipoMaterial;

@Entity
@Table(name = "instrucciones_reciclaje")
public class IntruccionesReciclaje {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_instruccion;

    @ManyToOne
    @JoinColumn(name = "id_material")
    private TipoMaterial material;

    private Integer paso_numero;
    private String instruccion;
    private String imagen_url;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

	public Long getId_instruccion() {
		return id_instruccion;
	}

	public void setId_instruccion(Long id_instruccion) {
		this.id_instruccion = id_instruccion;
	}

	public TipoMaterial getMaterial() {
		return material;
	}

	public void setMaterial(TipoMaterial material) {
		this.material = material;
	}

	public Integer getPaso_numero() {
		return paso_numero;
	}

	public void setPaso_numero(Integer paso_numero) {
		this.paso_numero = paso_numero;
	}

	public String getInstruccion() {
		return instruccion;
	}

	public void setInstruccion(String instruccion) {
		this.instruccion = instruccion;
	}

	public String getImagen_url() {
		return imagen_url;
	}

	public void setImagen_url(String imagen_url) {
		this.imagen_url = imagen_url;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}

    
}
