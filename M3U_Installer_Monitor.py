#!/usr/bin/env python3
"""
M3U Matrix CDS v5.0 – ENHANCED INSTALL MONITOR
- Triple-error tracking with severity levels
- Automatic retry mechanisms
- Expanded file system diagnostics
- Network connectivity checks
- Detailed failure analysis
- Smart recovery suggestions
"""

import os
import sys
import subprocess
import threading
import time
import json
import shutil
import psutil
from datetime import datetime
from pathlib import Path
import requests
import tempfile

# =============================================================================
# CONFIG - ENHANCED MONITORING
# =============================================================================
APP_NAME = "M3U Matrix CDS v5.0"
DESKTOP = Path.home() / "Desktop"
INSTALL_DIR = DESKTOP / APP_NAME
BAT_FILE = Path("installer m3u builder.bat")
LOG_FILE = INSTALL_DIR / "install_audit.log"
REPORT_FILE = INSTALL_DIR / "AUDIT_REPORT.txt"
DIAGNOSTICS_FILE = INSTALL_DIR / "SYSTEM_DIAGNOSTICS.json"

# Expected files for verification
EXPECTED_FILES = [
    "main.py",
    "gemini_api.py", 
    "imdb_scraper.py",
    "requirements.txt",
    "build_installer.py",
    "weebly_player_full.html",
    "player/player-logic.js",
    "themes/dark.json",
    "themes/neon.json",
    "electron_app/main.js",
    "electron_app/preload.js", 
    "electron_app/package.json"
]

# =============================================================================
# ENHANCED LOGGING WITH ERROR LEVELS
# =============================================================================
class ErrorTracker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.retries = {}
        self.severity_levels = {
            "LOW": "Minor issue - doesn't affect functionality",
            "MEDIUM": "Some features may be limited", 
            "HIGH": "Critical functionality missing",
            "CRITICAL": "Installation failed"
        }
    
    def add_error(self, category, error, severity="MEDIUM", suggestion=""):
        error_data = {
            "category": category,
            "error": str(error),
            "severity": severity,
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat(),
            "retry_count": self.retries.get(category, 0)
        }
        self.errors.append(error_data)
        return error_data
    
    def add_warning(self, category, warning, suggestion=""):
        warning_data = {
            "category": category,
            "warning": str(warning),
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat()
        }
        self.warnings.append(warning_data)
        return warning_data
    
    def increment_retry(self, category):
        self.retries[category] = self.retries.get(category, 0) + 1
    
    def get_retry_count(self, category):
        return self.retries.get(category, 0)

error_tracker = ErrorTracker()

def safe_log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {level}: {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
        print(line.strip())
    except Exception as e:
        print(f"[LOG ERROR] {e}")

# =============================================================================
# ENHANCED AUDIT TRACKER WITH RETRY SUPPORT
# =============================================================================
audit = {
    "start_time": datetime.now().isoformat(),
    "steps": [],
    "attempts": {},
    "system_info": {},
    "end_time": None,
    "success": True
}

def add_step(name, status="RUNNING", details="", attempt=1):
    step_data = {
        "name": name,
        "status": status,
        "details": details,
        "attempt": attempt,
        "time": datetime.now().isoformat()
    }
    audit["steps"].append(step_data)
    safe_log(f"{status}: {name} (Attempt {attempt}) — {details}")

# =============================================================================
# SYSTEM DIAGNOSTICS
# =============================================================================
def run_system_diagnostics():
    """Comprehensive system health check"""
    add_step("Run system diagnostics")
    
    diagnostics = {
        "timestamp": datetime.now().isoformat(),
        "system": {},
        "disk": {},
        "network": {},
        "python": {},
        "issues": []
    }
    
    try:
        # System info
        diagnostics["system"]["platform"] = sys.platform
        diagnostics["system"]["python_version"] = sys.version
        diagnostics["system"]["desktop_path"] = str(DESKTOP)
        diagnostics["system"]["installer_path"] = str(BAT_FILE)
        
        # Disk space check
        disk = psutil.disk_usage(str(DESKTOP))
        diagnostics["disk"]["free_gb"] = round(disk.free / (1024**3), 2)
        diagnostics["disk"]["total_gb"] = round(disk.total / (1024**3), 2)
        diagnostics["disk"]["percent_free"] = round(disk.percent, 2)
        
        if disk.percent > 90:
            error_tracker.add_warning(
                "Disk Space", 
                f"Low disk space: {disk.percent}% used",
                "Free up space on your desktop drive"
            )
        
        # Network check
        try:
            response = requests.get("https://www.google.com", timeout=10)
            diagnostics["network"]["internet_access"] = True
        except:
            diagnostics["network"]["internet_access"] = False
            error_tracker.add_error(
                "Network", 
                "No internet connection",
                "HIGH",
                "Check your internet connection and try again"
            )
        
        # Python environment
        diagnostics["python"]["executable"] = sys.executable
        diagnostics["python"]["path"] = sys.path
        
        # Save diagnostics
        with open(DIAGNOSTICS_FILE, "w", encoding="utf-8") as f:
            json.dump(diagnostics, f, indent=2)
            
        add_step("Run system diagnostics", "SUCCESS", f"Saved to {DIAGNOSTICS_FILE}")
        return diagnostics
        
    except Exception as e:
        error_tracker.add_error("Diagnostics", e, "LOW")
        add_step("Run system diagnostics", "FAILED", str(e))
        return diagnostics

# =============================================================================
# ENHANCED INSTALLER VERIFICATION
# =============================================================================
def verify_installer_comprehensive():
    """Triple-check installer integrity"""
    add_step("Comprehensive installer verification")
    
    checks = {
        "exists": False,
        "size_bytes": 0,
        "is_batch_file": False,
        "content_check": False,
        "encoding_valid": False
    }
    
    try:
        # Check 1: File exists
        if not BAT_FILE.exists():
            error_tracker.add_error(
                "Installer Verification",
                f"File not found: {BAT_FILE}",
                "CRITICAL",
                f"Ensure 'installer m3u builder.bat' is in: {Path.cwd()}"
            )
            return False
        checks["exists"] = True
        
        # Check 2: File size
        file_size = BAT_FILE.stat().st_size
        checks["size_bytes"] = file_size
        if file_size < 100:  # Less than 100 bytes is suspicious
            error_tracker.add_warning(
                "Installer Size",
                f"Installer file very small: {file_size} bytes",
                "File may be corrupted or incomplete"
            )
        
        # Check 3: File extension
        checks["is_batch_file"] = BAT_FILE.suffix.lower() == '.bat'
        
        # Check 4: Content validation
        try:
            content = BAT_FILE.read_text(encoding='utf-8')
            checks["content_check"] = True
            checks["encoding_valid"] = True
            
            # Check for key markers in batch file
            key_markers = ["@echo off", "M3U Matrix", "pip install", "python"]
            markers_found = [marker for marker in key_markers if marker in content]
            
            if len(markers_found) < 2:
                error_tracker.add_warning(
                    "Installer Content",
                    "Missing expected batch file markers",
                    "File may not be a valid installer"
                )
                
        except UnicodeDecodeError:
            checks["encoding_valid"] = False
            error_tracker.add_error(
                "Installer Encoding",
                "Batch file has invalid encoding",
                "HIGH",
                "Re-download the installer file"
            )
            return False
            
        add_step("Comprehensive installer verification", "SUCCESS", 
                f"Size: {file_size} bytes, Markers: {len(markers_found)}/4")
        return True
        
    except Exception as e:
        error_tracker.add_error("Installer Verification", e, "HIGH")
        return False

# =============================================================================
# ENHANCED INSTALLATION VERIFICATION
# =============================================================================
def verify_installation_comprehensive():
    """Triple-layer installation verification"""
    add_step("Comprehensive installation verification")
    
    verification = {
        "files_found": [],
        "files_missing": [],
        "files_partial": [],
        "total_expected": len(EXPECTED_FILES),
        "directory_structure": {},
        "install_size_bytes": 0
    }
    
    try:
        # Check if installation directory exists at all
        if not INSTALL_DIR.exists():
            error_tracker.add_error(
                "Installation Directory",
                f"Installation directory not created: {INSTALL_DIR}",
                "CRITICAL",
                "The installer may have failed at folder creation step"
            )
            return verification
        
        # Count total installation size
        total_size = 0
        for file_path in INSTALL_DIR.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        verification["install_size_bytes"] = total_size
        
        # Check each expected file
        for file_path in EXPECTED_FILES:
            full_path = INSTALL_DIR / file_path
            
            if full_path.exists():
                file_size = full_path.stat().st_size
                verification["files_found"].append({
                    "path": file_path,
                    "size_bytes": file_size,
                    "is_empty": file_size == 0
                })
                
                if file_size == 0:
                    verification["files_partial"].append(file_path)
                    error_tracker.add_warning(
                        "File Content",
                        f"Empty file: {file_path}",
                        "File was created but contains no data"
                    )
            else:
                verification["files_missing"].append(file_path)
        
        # Analyze results
        found_count = len(verification["files_found"])
        missing_count = len(verification["files_missing"])
        empty_count = len(verification["files_partial"])
        
        safe_log(f"Installation Analysis: {found_count} found, {missing_count} missing, {empty_count} empty")
        
        if missing_count > 0:
            error_tracker.add_error(
                "File Verification",
                f"{missing_count} files missing, {empty_count} files empty",
                "HIGH" if missing_count > 5 else "MEDIUM",
                "Check network connection and GitHub availability"
            )
            
        if found_count == 0:
            error_tracker.add_error(
                "Installation",
                "No expected files were installed",
                "CRITICAL",
                "The installer may be downloading to wrong location or failing completely"
            )
        
        add_step("Comprehensive installation verification", 
                "SUCCESS" if missing_count == 0 else "WARNING",
                f"Files: {found_count}/{len(EXPECTED_FILES)} found, Size: {total_size} bytes")
        
        return verification
        
    except Exception as e:
        error_tracker.add_error("Installation Verification", e, "HIGH")
        return verification

# =============================================================================
# SMART RETRY MECHANISM
# =============================================================================
def run_installer_with_retries(max_attempts=3):
    """Run installer with automatic retry on failure"""
    
    for attempt in range(1, max_attempts + 1):
        error_tracker.increment_retry("Installer Execution")
        add_step(f"Run installer - Attempt {attempt}", "RUNNING", "", attempt)
        
        safe_log(f"Starting installer attempt {attempt}/{max_attempts}")
        
        try:
            # Run the installer
            proc = subprocess.Popen(
                ['cmd', '/c', str(BAT_FILE)],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=Path.cwd()
            )
            
            # Extended monitoring with progress updates
            max_wait = 300  # 5 minutes
            for i in range(max_wait):
                time.sleep(1)
                if proc.poll() is not None:
                    break
                if i % 30 == 0:
                    safe_log(f"Installer running... ({i}s, attempt {attempt})")
            
            # Check result
            return_code = proc.poll()
            
            if return_code == 0:
                add_step(f"Run installer - Attempt {attempt}", "SUCCESS", 
                        f"Completed on attempt {attempt}")
                safe_log(f"Installer completed successfully on attempt {attempt}")
                return True
            else:
                status_msg = f"Exit code: {return_code}" if return_code is not None else "Timed out"
                add_step(f"Run installer - Attempt {attempt}", "FAILED", status_msg)
                
                error_data = error_tracker.add_error(
                    "Installer Execution",
                    f"Attempt {attempt} failed: {status_msg}",
                    "HIGH" if attempt == max_attempts else "MEDIUM",
                    f"Retrying... ({attempt}/{max_attempts})" if attempt < max_attempts else "All retries exhausted"
                )
                
                if attempt < max_attempts:
                    safe_log(f"Waiting 5 seconds before retry {attempt + 1}...")
                    time.sleep(5)
                else:
                    safe_log("All installation attempts failed")
                    return False
                    
        except Exception as e:
            error_tracker.add_error(
                "Installer Execution",
                f"Attempt {attempt} crashed: {str(e)}",
                "HIGH" if attempt == max_attempts else "MEDIUM"
            )
            if attempt < max_attempts:
                time.sleep(5)
            else:
                return False
    
    return False

# =============================================================================
# ENHANCED REPORT GENERATION
# =============================================================================
def generate_comprehensive_report():
    """Generate detailed report with error analysis and recommendations"""
    audit["end_time"] = datetime.now().isoformat()
    
    # Calculate duration
    start_dt = datetime.fromisoformat(audit['start_time'])
    end_dt = datetime.fromisoformat(audit['end_time'])
    duration = end_dt - start_dt
    
    # Error analysis
    error_summary = {
        "total_errors": len(error_tracker.errors),
        "total_warnings": len(error_tracker.warnings),
        "by_severity": {},
        "by_category": {}
    }
    
    for error in error_tracker.errors:
        error_summary["by_severity"][error["severity"]] = error_summary["by_severity"].get(error["severity"], 0) + 1
        error_summary["by_category"][error["category"]] = error_summary["by_category"].get(error["category"], 0) + 1
    
    # Build comprehensive report
    report = f"""
╔════════════════════════════════════════════════════════════╗
║          M3U MATRIX CDS v5.0 - ENHANCED AUDIT REPORT       ║
╚════════════════════════════════════════════════════════════╝

TIMELINE:
  Start    : {audit['start_time']}
  End      : {audit['end_time']}
  Duration : {duration}

SUMMARY:
  Success  : {'✅ YES' if audit['success'] else '❌ NO'}
  Errors   : {error_summary['total_errors']}
  Warnings : {error_summary['total_warnings']}

ERROR SEVERITY BREAKDOWN:
"""
    
    for severity, count in error_summary["by_severity"].items():
        report += f"  {severity}: {count} error(s)\n"

    report += f"""
ERROR CATEGORIES:
"""
    for category, count in error_summary["by_category"].items():
        report += f"  {category}: {count} error(s)\n"

    report += f"""
DETAILED STEPS:
"""
    for step in audit["steps"]:
        status_icon = "✅" if step["status"] == "SUCCESS" else "⚠️" if step["status"] == "WARNING" else "❌"
        report += f"  {status_icon} [{step['status']}] {step['name']}\n"
        if step["details"]:
            report += f"      → {step['details']}\n"
        if step.get("attempt", 1) > 1:
            report += f"      → Attempt: {step['attempt']}\n"

    if error_tracker.errors:
        report += f"""
CRITICAL ERRORS:
"""
        for error in error_tracker.errors:
            if error["severity"] in ["HIGH", "CRITICAL"]:
                report += f"  🚨 {error['category']}: {error['error']}\n"
                if error["suggestion"]:
                    report += f"      💡 Suggestion: {error['suggestion']}\n"

    if error_tracker.warnings:
        report += f"""
WARNINGS:
"""
        for warning in error_tracker.warnings:
            report += f"  ⚠️  {warning['category']}: {warning['warning']}\n"
            if warning["suggestion"]:
                report += f"      💡 Suggestion: {warning['suggestion']}\n"

    report += f"""
RECOMMENDATIONS:
"""
    
    # Smart recommendations based on error analysis
    recommendations = []
    
    if any("Network" in error["category"] for error in error_tracker.errors):
        recommendations.append("• Check your internet connection and firewall settings")
    
    if any("Installer" in error["category"] for error in error_tracker.errors):
        recommendations.append("• Verify the installer file is complete and not corrupted")
    
    if any("Disk" in error["category"] for error in error_tracker.warnings):
        recommendations.append("• Free up disk space on your desktop drive")
    
    if any("File Verification" in error["category"] for error in error_tracker.errors):
        recommendations.append("• The installer may be blocked from downloading files")
        recommendations.append("• Try running as Administrator")
        recommendations.append("• Check antivirus software isn't blocking the installation")
    
    if not recommendations:
        if audit['success']:
            recommendations.append("• Installation completed successfully!")
            recommendations.append("• Run: START M3U Matrix.bat")
        else:
            recommendations.append("• Review the errors above and try again")
            recommendations.append("• Contact support with the audit log")
    
    for rec in recommendations:
        report += f"  {rec}\n"

    report += f"""
FILES:
  Log          : {LOG_FILE}
  Report       : {REPORT_FILE}
  Diagnostics  : {DIAGNOSTICS_FILE}
  Installer    : {BAT_FILE}
  Location     : {INSTALL_DIR}

Thank you for using M3U Matrix CDS v5.0!
"""
    
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report)
        safe_log(f"Comprehensive audit report saved: {REPORT_FILE}")
        return report
    except Exception as e:
        safe_log(f"Failed to save report: {e}")
        return report

# =============================================================================
# MAIN EXECUTION WITH ENHANCED MONITORING
# =============================================================================
def main():
    safe_log("=== ENHANCED M3U INSTALL MONITOR STARTED ===")
    
    print("\n" + "="*70)
    print("   M3U MATRIX CDS v5.0 - ENHANCED INSTALL MONITOR")
    print("="*70)
    print(f"🔍 Monitoring: {BAT_FILE}")
    print(f"📁 Installing to: {INSTALL_DIR}")
    print(f"🔄 Automatic retries: 3 attempts")
    print("="*70)

    try:
        # Step 1: System Diagnostics
        diagnostics = run_system_diagnostics()
        
        # Step 2: Comprehensive Installer Verification
        if not verify_installer_comprehensive():
            print("\n❌ CRITICAL: Installer verification failed!")
            print("   Please check the errors above.")
            input("\nPress Enter to exit...")
            return

        # Step 3: Create Installation Folder
        add_step("Create installation folder")
        try:
            if INSTALL_DIR.exists():
                safe_log("Removing old installation folder...")
                shutil.rmtree(INSTALL_DIR, ignore_errors=True)
                time.sleep(2)
            INSTALL_DIR.mkdir(parents=True, exist_ok=True)
            add_step("Create installation folder", "SUCCESS", f"Created: {INSTALL_DIR}")
        except Exception as e:
            error_tracker.add_error("Folder Creation", e, "HIGH")
            add_step("Create installation folder", "FAILED", str(e))

        # Ask user before proceeding
        print("\n" + "="*70)
        print("   READY FOR ENHANCED INSTALLATION")
        print("="*70)
        print("The enhanced monitor will:")
        print("  • Run comprehensive system checks")
        print("  • Attempt installation up to 3 times if needed")
        print("  • Provide detailed error analysis")
        print("  • Generate smart recovery suggestions")
        print(f"\nInstaller: {BAT_FILE.name}")
        print(f"Location:  {INSTALL_DIR}")
        
        choice = input("\nProceed with enhanced installation? [Y]es / [N]o: ").strip().lower()

        if choice not in ['y', 'yes']:
            safe_log("User cancelled enhanced installation")
            print("\nInstallation cancelled.")
            print("You can run the installer manually later.")
            return

        # Step 4: Run Installer with Retries
        safe_log("Starting enhanced installation with retry support...")
        installation_success = run_installer_with_retries(max_attempts=3)
        
        # Step 5: Comprehensive Verification
        verification = verify_installation_comprehensive()
        
        # Determine overall success
        audit["success"] = installation_success and len(verification["files_missing"]) == 0
        
        # Step 6: Generate Comprehensive Report
        report = generate_comprehensive_report()
        safe_log("=== ENHANCED MONITORING COMPLETED ===")

        # Final User Feedback
        print("\n" + "="*70)
        print("   ENHANCED INSTALLATION AUDIT COMPLETE")
        print("="*70)
        
        if audit["success"]:
            print("✅ SUCCESS! Application is ready to use.")
            print("   Run: START M3U Matrix.bat")
        else:
            print("⚠️  Installation completed with issues.")
            print("   Review the recommendations below.")
        
        print(f"\n📊 Files installed: {len(verification['files_found'])}/{len(EXPECTED_FILES)}")
        print(f"📁 Location: {INSTALL_DIR}")
        print(f"📋 Report: {REPORT_FILE}")
        print(f"🔍 Diagnostics: {DIAGNOSTICS_FILE}")
        
        # Show quick recommendations
        if verification["files_missing"]:
            print(f"\n❌ Missing files: {len(verification['files_missing'])}")
            if len(verification["files_missing"]) > 5:
                print("   The installer may be downloading to wrong location")
                print("   Check network connectivity and GitHub access")
        
        print("\nPress Enter to view detailed report...")
        input()
        
        # Show report summary
        print("\n" + "="*70)
        print("DETAILED REPORT SUMMARY")
        print("="*70)
        print(report)
        
    except Exception as e:
        safe_log(f"CRITICAL FAILURE: {e}")
        error_tracker.add_error("Main Process", e, "CRITICAL")
        generate_comprehensive_report()
        print(f"\n💥 CRITICAL ERROR: {e}")
        print("   See audit log for details.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()