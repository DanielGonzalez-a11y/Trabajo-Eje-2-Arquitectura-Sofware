package com.eje2.trabajo.modelo;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import com.eje2.trabajo.modelo.TipoMaterial;

@Entity
@Table(name = "centros_materiales")
public class CentroMaterial {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_centro_material;

    @ManyToOne
    @JoinColumn(name = "id_centro")
    private CentroReciclaje centro;

    @ManyToOne
    @JoinColumn(name = "id_material")
    private TipoMaterial material;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

	public Long getId_centro_material() {
		return id_centro_material;
	}

	public void setId_centro_material(Long id_centro_material) {
		this.id_centro_material = id_centro_material;
	}

	public CentroReciclaje getCentro() {
		return centro;
	}

	public void setCentro(CentroReciclaje centro) {
		this.centro = centro;
	}

	public TipoMaterial getMaterial() {
		return material;
	}

	public void setMaterial(TipoMaterial material) {
		this.material = material;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}
    
}
