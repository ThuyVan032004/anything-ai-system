from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime
from emotion_analysis.data.models.ea_report_inputs_model import EAReportInputsModel


class EAProfilingHelper:
    @staticmethod
    def validate_data(inputs: EAReportInputsModel):
        # Validate data schema
        data_schema = inputs.data_schema
        
        schema_key_validation = True
        schema_data_type_validation = True
           
        keys = data_schema.keys()
        expected_keys = ["cleaned_text", "label"]
        
        if set(keys) != set(expected_keys):
            schema_key_validation = False
            
        if data_schema["cleaned_text"] != "object" or data_schema["label"] != "int64":
            schema_data_type_validation = False
        
        data_schema_validation = schema_key_validation and schema_data_type_validation
        
        # Validate missing values
        missing_values_threshold = 0.05  # 5% threshold
        missing_values_validation = {}
        missing_values_summary = inputs.missing_values_summary
        
        for key, value in missing_values_summary.items():
            if value["missing_percentage"] <= missing_values_threshold:
                missing_values_validation[key] = True
            else:
                missing_values_validation[key] = False
                
        # Validate corpus vocabulary
        vocabulary_profile = inputs.vocabulary_profile
        
        variety_threshold = 0.2  # 20% unique words
        vocabulary_variety = (vocabulary_profile.unique_words / vocabulary_profile.total_words)
        
        vocabulary_validation = vocabulary_variety >= variety_threshold
        
        # Validate corpus length
        length_profile = inputs.length_profile
        
        max_length_threshold = 100  # max 100 words
        min_length_threshold = 3    # min 3 words
        
        length_validation = (length_profile.max_length <= max_length_threshold and
                             length_profile.min_length >= min_length_threshold)
        
        # Validate corpus redundancy
        redundancy_profile = inputs.redundancy_profile
        
        redundancy_threshold = 0.2  # max 20% redundancy
        
        redundancy_validation = redundancy_profile.redundancy_ratio <= redundancy_threshold
        
        return {
            "data_schema_validation_result": {
                "is_valid": data_schema_validation,
                "details": {
                    "expected_columns": expected_keys,
                    "actual_columns": list(keys),
                    "expected_data_types": {
                        "cleaned_text": "object",
                        "label": "int64"
                    },
                    "actual_data_types": data_schema
                }
            },
            
            "missing_values_validation_result": {
                "is_valid": all(missing_values_validation.values()),
                "details": {
                    "missing_values_threshold": missing_values_threshold,
                    "missing_values_summary": missing_values_summary,
                }
            },
            
            "vocabulary_validation_result": {
                "is_valid": vocabulary_validation,
                "details": {
                    "vocabulary_variety": vocabulary_variety,
                    "variety_threshold": variety_threshold
                }
            },
            
            "length_validation_result": {
                "is_valid": length_validation,
                "details": {
                    "max_length": length_profile.max_length,
                    "min_length": length_profile.min_length,
                    "mean_length": length_profile.mean_length,
                    "median_length": length_profile.median_length,
                    "standard_deviation": length_profile.standard_deviation,
                    "max_length_threshold": max_length_threshold,
                    "min_length_threshold": min_length_threshold
                }
            },
            
            "redundancy_validation_result": {
                "is_valid": redundancy_validation,
                "details": {
                    "redundancy_ratio": redundancy_profile.redundancy_ratio,
                    "redundancy_threshold": redundancy_threshold
                }
            }
        }
        
        
    @staticmethod
    def generate_report(data_validation_result, output_path: str = f"ea_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"):
        """
        Generate a PDF report from data validation results.
        
        Args:
            data_validation_result: Dictionary with validation results
            output_path: Path where the PDF will be saved
        """
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1f4788"),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#2e5c8a"),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Add title
        story.append(Paragraph("Data Validation Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))
        
        # Overall status
        all_valid = all(
            result.get("is_valid", False) 
            for result in data_validation_result.values()
        )
        status_color = colors.green if all_valid else colors.red
        status_text = "✓ ALL VALIDATIONS PASSED" if all_valid else "✗ SOME VALIDATIONS FAILED"
        story.append(Paragraph(f"<font color='{status_color}'><b>{status_text}</b></font>", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        
        # Data Schema Validation
        story.append(Paragraph("1. Data Schema Validation", heading_style))
        schema_result = data_validation_result["data_schema_validation_result"]
        schema_details = schema_result["details"]
        
        schema_data = [
            ["Aspect", "Expected", "Actual", "Status"],
            ["Columns", str(schema_details["expected_columns"]), str(schema_details["actual_columns"]), 
             "✓" if schema_result["is_valid"] else "✗"],
            ["Data Types", str(schema_details["expected_data_types"]), str(schema_details["actual_data_types"]), ""]
        ]
        
        schema_table = Table(schema_data, colWidths=[1.5*inch, 2*inch, 2*inch, 0.5*inch])
        schema_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e5c8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ]))
        story.append(schema_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Missing Values Validation
        story.append(Paragraph("2. Missing Values Validation", heading_style))
        mv_result = data_validation_result["missing_values_validation_result"]
        mv_details = mv_result["details"]
        
        story.append(Paragraph(f"<b>Threshold:</b> {mv_details['missing_values_threshold']*100}%", styles["Normal"]))
        
        mv_summary = mv_details["missing_values_summary"]
        mv_data = [["Column", "Missing Count", "Missing Percentage", "Status"]]
        for col, values in mv_summary.items():
            missing_pct = values.get("missing_percentage", 0) * 100
            status = "✓ Pass" if values.get("missing_percentage", 0) <= mv_details['missing_values_threshold'] else "✗ Fail"
            mv_data.append([col, str(values.get("missing_count", 0)), f"{missing_pct:.2f}%", status])
        
        mv_table = Table(mv_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        mv_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e5c8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ]))
        story.append(mv_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Vocabulary Validation
        story.append(Paragraph("3. Vocabulary Validation", heading_style))
        vocab_result = data_validation_result["vocabulary_validation_result"]
        vocab_details = vocab_result["details"]
        
        vocab_data = [
            ["Metric", "Value", "Threshold", "Status"],
            ["Vocabulary Variety", f"{vocab_details['vocabulary_variety']:.4f}", 
             f"{vocab_details['variety_threshold']}", "✓" if vocab_result["is_valid"] else "✗"]
        ]
        
        vocab_table = Table(vocab_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        vocab_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e5c8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ]))
        story.append(vocab_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Length Validation
        story.append(Paragraph("4. Corpus Length Validation", heading_style))
        length_result = data_validation_result["length_validation_result"]
        length_details = length_result["details"]
        
        length_data = [
            ["Metric", "Value", "Threshold", "Status"],
            ["Min Length", f"{length_details['min_length']}", 
             f">= {length_details['min_length_threshold']}", "✓" if length_details['min_length'] >= length_details['min_length_threshold'] else "✗"],
            ["Max Length", f"{length_details['max_length']}", 
             f"<= {length_details['max_length_threshold']}", "✓" if length_details['max_length'] <= length_details['max_length_threshold'] else "✗"],
            ["Mean Length", f"{length_details['mean_length']:.2f}", "-", "-"],
            ["Median Length", f"{length_details['median_length']}", "-", "-"],
            ["Std Deviation", f"{length_details['standard_deviation']:.2f}", "-", "-"]
        ]
        
        length_table = Table(length_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        length_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e5c8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ]))
        story.append(length_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Redundancy Validation
        story.append(Paragraph("5. Corpus Redundancy Validation", heading_style))
        redund_result = data_validation_result["redundancy_validation_result"]
        redund_details = redund_result["details"]
        
        redund_data = [
            ["Metric", "Value", "Threshold", "Status"],
            ["Redundancy Ratio", f"{redund_details['redundancy_ratio']:.4f}", 
             f"<= {redund_details['redundancy_threshold']}", "✓" if redund_result["is_valid"] else "✗"]
        ]
        
        redund_table = Table(redund_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        redund_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e5c8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ]))
        story.append(redund_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Summary
        story.append(Paragraph("Summary", heading_style))
        summary_text = f"""
        <b>Total Validations:</b> 5<br/>
        <b>Passed:</b> {sum(1 for result in data_validation_result.values() if result.get("is_valid", False))}<br/>
        <b>Failed:</b> {sum(1 for result in data_validation_result.values() if not result.get("is_valid", False))}<br/>
        <b>Overall Status:</b> <font color="{status_color}"><b>{"PASSED" if all_valid else "FAILED"}</b></font>
        """
        story.append(Paragraph(summary_text, styles["Normal"]))
        
        # Build PDF
        doc.build(story)
        print(f"PDF report generated successfully: {output_path}")
        
        return output_path
        
        
        
        
        
        
        
        