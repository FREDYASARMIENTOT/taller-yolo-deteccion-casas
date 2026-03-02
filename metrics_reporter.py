"""
Script para visualizar las métricas del modelo YOLOv8 de detección de casas.

Este script lee el archivo metrics.json y presenta las métricas de forma legible
y formateada, facilitando la presentación de resultados.
"""

import json
from pathlib import Path
from typing import Dict, Any


class MetricsReporter:
    """Clase para reportar las métricas del modelo entrenado."""
    
    def __init__(self, metrics_file: str = "metrics.json"):
        """
        Inicializa el reporter de métricas.
        
        Args:
            metrics_file: Ruta al archivo de métricas JSON
        """
        self.metrics_file = Path(metrics_file)
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Carga las métricas desde el archivo JSON."""
        if not self.metrics_file.exists():
            raise FileNotFoundError(f"Archivo de métricas no encontrado: {self.metrics_file}")
        
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def print_header(self, title: str) -> None:
        """Imprime un encabezado formateado."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_section(self, title: str) -> None:
        """Imprime un título de sección."""
        print(f"\n📊 {title}")
        print("-" * 60)
    
    def print_metrics(self) -> None:
        """Imprime todas las métricas de forma formateada."""
        # Encabezado principal
        self.print_header("MÉTRICAS DEL MODELO YOLOV8 - DETECCIÓN DE CASAS")
        
        # Información general del modelo
        model_info = self.metrics["model_metrics"]
        self.print_section("Información del Modelo")
        print(f"Nombre:      {model_info['name']}")
        print(f"Arquitectura: {model_info['model_weights']['architecture']}")
        print(f"Ruta:        {model_info['model_weights']['path']}")
        
        # Métricas de desempeño
        self.print_section("Métricas de Desempeño")
        performance = model_info["performance"]
        
        print(f"mAP@50:      {performance['mAP@50']:.4f} ({performance['mAP@50']*100:.2f}%)")
        print(f"mAP@50-95:   {performance['mAP@50-95']:.4f} ({performance['mAP@50-95']*100:.2f}%)")
        print(f"Precision:   {performance['precision']:.4f} ({performance['precision']*100:.2f}%)")
        print(f"Recall:      {performance['recall']:.4f} ({performance['recall']*100:.2f}%)")
        
        # Resumen de desempeño
        summary = model_info["performance_summary"]
        self.print_section("Resumen de Desempeño")
        print(f"Estado:      ✅ {summary['status']}")
        print(f"Descripción: {summary['description']}")
        print(f"Precisión:   {summary['accuracy_percentage']:.2f}%")
        
        # Detalles de entrenamiento
        self.print_section("Detalles del Entrenamiento")
        training = model_info["training_details"]
        print(f"Modelo Base:     {training['model_base']}")
        print(f"Hardware:        {training['hardware']}")
        print(f"Épocas:          {training['epochs']}")
        print(f"Dataset:         {training['dataset']}")
        print(f"Clases:          {training['num_classes']}")
        print(f"Nombres:         {', '.join(training['class_names'])}")
        
        # Configuración de inferencia
        self.print_section("Configuración de Inferencia")
        inference = self.metrics["inference_metrics"]
        print(f"Confianza Por Defecto: {inference['confidence_threshold_default']}")
        print(f"Formatos Soportados:   {', '.join(inference['supported_formats'])}")
        print(f"Velocidad:             {inference['model_inference_speed']}")
        
        # Pie de página
        print("\n" + "=" * 60)
        print(f"Generado: {self.metrics['generated_at']}")
        print(f"Versión:  {self.metrics['version']}")
        print("=" * 60 + "\n")
    
    def get_json_export(self) -> str:
        """Retorna las métricas en formato JSON formateado."""
        return json.dumps(self.metrics, indent=2, ensure_ascii=False)
    
    def save_text_report(self, output_file: str = "metrics_report.txt") -> None:
        """Guarda el reporte de métricas en un archivo de texto."""
        import sys
        import io
        
        # Capturar la salida
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        self.print_metrics()
        
        # Restaurar stdout
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Guardar en archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"✅ Reporte guardado en: {output_file}")
    
    def get_metric_by_key(self, key: str) -> Any:
        """Obtiene una métrica específica por clave."""
        keys = key.split('.')
        value = self.metrics
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return None


def main():
    """Función principal para ejecutar el reporte de métricas."""
    try:
        reporter = MetricsReporter("metrics.json")
        
        # Mostrar métricas en consola
        reporter.print_metrics()
        
        # Guardar reporte en archivo de texto
        reporter.save_text_report("metrics_report.txt")
        
        # Mostrar algunas métricas específicas
        print("\n📌 Ejemplos de acceso a métricas:")
        print(f"   mAP@50: {reporter.get_metric_by_key('model_metrics.performance.mAP@50')}")
        print(f"   Precision: {reporter.get_metric_by_key('model_metrics.performance.precision')}")
        print(f"   Recall: {reporter.get_metric_by_key('model_metrics.performance.recall')}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
