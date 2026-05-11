from __future__ import annotations

from optiscaler_gui.domain.models import (
    InjectionPlan,
    InjectionRequest,
    InjectionStep,
    OperationResult,
)


class BaseStubInjectionBackend:
    platform_name = "unknown"

    def create_plan(self, request: InjectionRequest) -> InjectionPlan:
        steps = (
            InjectionStep("Validate selected game directory", destination=request.game.install_dir),
            InjectionStep("Validate selected OptiScaler package", source=request.package.root_dir),
            InjectionStep("Create backup of files that would be replaced"),
            InjectionStep("Apply OptiScaler files using the platform backend"),
        )
        return InjectionPlan(request=request, steps=steps)

    def apply_plan(self, plan: InjectionPlan) -> OperationResult:
        return OperationResult(
            succeeded=False,
            message=f"{self.platform_name} injection backend is not implemented yet.",
            details=tuple(step.label for step in plan.steps),
        )
