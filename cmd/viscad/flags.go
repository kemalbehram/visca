// Copyright 2021 Visca Foundation
// This file is part of Visca' Visca library.
//
// The Visca library is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// The Visca library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with the Visca library. If not, see https://github.com/onchainengineer/visca/blob/main/LICENSE
package main

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/onchainengineer/visca/version"
)

const flagLong = "long"

func init() {
	infoCmd.Flags().Bool(flagLong, false, "Print full information")
}

var infoCmd = &cobra.Command{
	Use:   "info",
	Short: "Print version info",
	RunE: func(_ *cobra.Command, _ []string) error {
		fmt.Println(version.Version())
		return nil
	},
}
